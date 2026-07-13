import pandas as pd


def validate_time_series(df, date_column, target_column):
    """
    Validate the dataset for time series forecasting.
    """

    result = {}

    # Check if required columns exist
    if date_column not in df.columns:
        result["is_valid"] = False
        result["error"] = "Date column not found."
        return result

    if target_column not in df.columns:
        result["is_valid"] = False
        result["error"] = "Target column not found."
        return result

    # Convert date column
    df[date_column] = pd.to_datetime(df[date_column], errors="coerce")

    # Sort data
    df = df.sort_values(by=date_column)

    # Count invalid dates
    invalid_dates = int(df[date_column].isnull().sum())

    # Infer frequency
    frequency = pd.infer_freq(df[date_column])

    if frequency is None:
        frequency = "Unknown"

    result = {
        "is_valid": True,
        "date_column": date_column,
        "target_column": target_column,
        "total_periods": len(df),
        "invalid_dates": invalid_dates,
        "frequency": frequency
    }

    return result