import pandas as pd

def test_csv_structure():
    """
    Verify that the sample CSV contains required columns.
    """
    # Adjust path if needed
    df = pd.read_csv("data/solar_data.csv")
    required_cols = {"hour", "solar_output", "city_demand"}
    assert required_cols.issubset(df.columns), "CSV is missing required columns"

def test_basic_math():
    """
    Simple sanity test to ensure pytest is running correctly.
    """
    assert 2 + 2 == 4

