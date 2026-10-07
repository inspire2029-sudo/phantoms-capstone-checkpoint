from __future__ import annotations

import io
import sqlite3
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

KAGGLE_URL = "https://www.kaggle.com/api/v1/datasets/download/yasserh/titanic-dataset"


def download_titanic(output_dir: str | Path = "data/raw") -> Path:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    csv_path = output / "Titanic-Dataset.csv"

    if csv_path.exists():
        return csv_path

    request = Request(KAGGLE_URL, headers={"User-Agent": "PHANTOMS-capstone"})
    with urlopen(request, timeout=30) as response:
        payload = response.read()

    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        candidates = [name for name in archive.namelist() if name.lower().endswith(".csv")]
        if not candidates:
            raise RuntimeError("No CSV file found in the Kaggle dataset.")
        with archive.open(candidates[0]) as source, csv_path.open("wb") as target:
            target.write(source.read())

    return csv_path


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Remove columns that are identifiers or too sparse/high-cardinality for this checkpoint.
    drop_columns = [c for c in ["PassengerId", "Name", "Ticket", "Cabin"] if c in df.columns]
    df = df.drop(columns=drop_columns)

    if "Age" in df.columns:
        df["Age"] = df["Age"].fillna(df["Age"].median())

    if "Fare" in df.columns:
        df["Fare"] = df["Fare"].fillna(df["Fare"].median())

    if "Embarked" in df.columns:
        df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode().iloc[0])

    return df


def build_sqlite(csv_path: str | Path, db_path: str | Path = "data/titanic.db") -> Path:
    csv_path = Path(csv_path)
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    raw = pd.read_csv(csv_path)
    cleaned = clean_data(raw)

    with sqlite3.connect(db_path) as conn:
        raw.to_sql("titanic_raw", conn, if_exists="replace", index=False)
        cleaned.to_sql("titanic_cleaned", conn, if_exists="replace", index=False)

    return db_path


def main() -> None:
    csv_path = download_titanic()
    db_path = build_sqlite(csv_path)
    print(f"Dataset: {csv_path}")
    print(f"SQLite DB: {db_path}")


if __name__ == "__main__":
    main()
