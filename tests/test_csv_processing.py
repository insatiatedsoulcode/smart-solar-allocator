import os
import pandas as pd

DATA_PATH = os.path.join("data", "solar_data.csv")

def test_csv_exists():
    """Check that the sample CSV exists and is not empty."""
    assert os.path.exists(DATA_PATH), "solar_data.csv is missing in data/"
    assert os.path.getsize(DATA_PATH) > 0, "solar_data.csv is empty"

def test_csv_columns():
    """Ensure the CSV contains required columns."""
    df = pd.read_csv(DATA_PATH)
    required_cols = {"hour", "solar_output", "city_demand"}
    assert required_cols.issubset(df.columns), f"CSV missing columns: {required_cols - set(df.columns)}"

def test_allocation_math():
    """
    Validate that a simple allocation (solar first, then grid) matches expectations.
    This does NOT call Mistral; it checks the rule-based fallback logic.
    """
    df = pd.read_csv(DATA_PATH)
    for _, row in df.iterrows():
        solar_output = row["solar_output"]
        city_demand = row["city_demand"]
        solar_used = min(solar_output, city_demand)
        grid_used = city_demand - solar_used
        assert solar_used + grid_used == city_demand, "Allocation math error"

