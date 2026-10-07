from pathlib import Path
import io
import sqlite3
import zipfile
from urllib.request import Request, urlopen

import pandas as pd

KAGGLE_URL = "https://www.kaggle.com/api/v1/datasets/download/yasserh/titanic-dataset"


def download_titanic(output_dir="data/raw"):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    csv_path = output / "Titanic-Dataset.csv"
    if csv_path.exists():
        return csv_path

    request = Request(KAGGLE_URL, headers={"User-Agent": "PHANTOMS-capstone"})
    with urlopen(request, timeout=30) as response:
        payload = response.read()

    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        csv_files = [name for name in archive.namelist() if name.lower().endswith(".csv")]
        if not csv_files:
            raise RuntimeError("No CSV file found in the Kaggle dataset.")
        with archive.open(csv_files[0]) as source, csv_path.open("wb") as target:
            target.write(source.read())
    return csv_path


def clean_data(df):
    df = df.copy()
    drop_columns = [c for c in ["PassengerId", "Name", "Ticket", "Cabin"] if c in df.columns]
    df = df.drop(columns=drop_columns)

    for column in ["Age", "Fare"]:
        if column in df.columns:
            df[column] = df[column].fillna(df[column].median())

    if "Embarked" in df.columns:
        df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode().iloc[0])
    return df


def build_sqlite(csv_path, db_path="data/titanic.db"):
    csv_path, db_path = Path(csv_path), Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    raw = pd.read_csv(csv_path)
    cleaned = clean_data(raw)

    with sqlite3.connect(db_path) as conn:
        raw.to_sql("titanic_raw", conn, if_exists="replace", index=False)
        cleaned.to_sql("titanic_cleaned", conn, if_exists="replace", index=False)
    return db_path


if __name__ == "__main__":
    csv = download_titanic()
    print(f"Dataset: {csv}")
    print(f"SQLite DB: {build_sqlite(csv)}")
