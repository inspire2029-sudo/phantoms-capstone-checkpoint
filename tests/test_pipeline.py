import pandas as pd

from src.pipeline import clean_data


def test_clean_data_removes_unhelpful_columns():
    df = pd.DataFrame(
        {
            "PassengerId": [1, 2],
            "Name": ["A", "B"],
            "Ticket": ["T1", "T2"],
            "Cabin": [None, None],
            "Age": [None, 20],
            "Fare": [10, None],
            "Embarked": ["S", None],
            "Survived": [0, 1],
        }
    )

    cleaned = clean_data(df)

    assert "PassengerId" not in cleaned.columns
    assert "Name" not in cleaned.columns
    assert "Ticket" not in cleaned.columns
    assert "Cabin" not in cleaned.columns
    assert cleaned["Age"].isna().sum() == 0
    assert cleaned["Fare"].isna().sum() == 0
    assert cleaned["Embarked"].isna().sum() == 0
