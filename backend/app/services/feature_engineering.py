import pandas as pd


def create_time_features(df, date_column):
    """
    Create useful time-based features from the date column.
    """

    df = df.copy()

    df[date_column] = pd.to_datetime(df[date_column])

    df["Year"] = df[date_column].dt.year
    df["Month"] = df[date_column].dt.month
    df["Day"] = df[date_column].dt.day
    df["Quarter"] = df[date_column].dt.quarter
    df["DayOfWeek"] = df[date_column].dt.dayofweek
    df["WeekOfYear"] = df[date_column].dt.isocalendar().week.astype(int)
    df["IsWeekend"] = (df["DayOfWeek"] >= 5).astype(int)

    return {
        "feature_columns": [
            "Year",
            "Month",
            "Day",
            "Quarter",
            "DayOfWeek",
            "WeekOfYear",
            "IsWeekend"
        ],
        "total_features_created": 7
    }