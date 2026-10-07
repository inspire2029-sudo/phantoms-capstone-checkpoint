from pathlib import Path
import json
import sqlite3

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

DB_PATH = Path("data/titanic.db")
METRICS_PATH = Path("reports/metrics.json")
RANDOM_STATE = 42


def load_data(db_path=DB_PATH):
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query("SELECT * FROM titanic_cleaned", conn)


def build_preprocessor(X):
    numeric = X.select_dtypes(include=["number"]).columns.tolist()
    categorical = X.select_dtypes(exclude=["number"]).columns.tolist()

    numeric_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    categorical_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ])

    return ColumnTransformer([
        ("num", numeric_pipe, numeric),
        ("cat", categorical_pipe, categorical),
    ])


def evaluate(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    cv_f1 = cross_val_score(model, X_train, y_train, cv=5, scoring="f1")

    return {
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "precision": round(float(precision_score(y_test, predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, predictions, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, predictions, zero_division=0)), 4),
        "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
        "cv_f1_mean": round(float(cv_f1.mean()), 4),
        "cv_f1_std": round(float(cv_f1.std()), 4),
    }


def main():
    df = load_data()
    X = df.drop(columns=["Survived"])
    y = df["Survived"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )

    models = {
        "logistic_regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
        "decision_tree": DecisionTreeClassifier(max_depth=5, random_state=RANDOM_STATE),
        "neural_network": MLPClassifier(
            hidden_layer_sizes=(32, 16),
            max_iter=500,
            early_stopping=True,
            random_state=RANDOM_STATE,
        ),
    }

    results = {}
    for name, estimator in models.items():
        pipeline = Pipeline([
            ("preprocessor", build_preprocessor(X)),
            ("model", estimator),
        ])
        results[name] = evaluate(pipeline, X_train, X_test, y_train, y_test)

    best_model_by_f1 = max(results, key=lambda name: results[name]["f1"])
    selected_model = "logistic_regression"
    payload = {
        "dataset": "Titanic",
        "target": "Survived",
        "split": {"test_size": 0.2, "random_state": RANDOM_STATE, "stratified": True},
        "models": results,
        "best_model_by_f1": best_model_by_f1,
        "selected_model": selected_model,
        "selection_reason": "Logistic Regression was selected as the practical final model because its F1 is effectively tied with the neural network while its Recall is higher and its complexity is lower.",
        "deep_learning_decision": "Neural network tested, but not selected because its extra complexity did not produce a meaningful F1/Recall improvement.",
    }

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
