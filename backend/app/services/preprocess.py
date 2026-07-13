import pandas as pd


def remove_duplicates(df):
    """
    Remove duplicate rows.
    """
    before = len(df)
    df = df.drop_duplicates()
    duplicates_removed = before - len(df)

    return df, duplicates_removed


def handle_missing_values(df):
    """
    Fill missing values.
    """

    numeric_columns = df.select_dtypes(include=["number"]).columns

    for col in numeric_columns:
        df[col] = df[col].fillna(df[col].median())

    categorical_columns = df.select_dtypes(include=["object"]).columns

    for col in categorical_columns:
        if not df[col].mode().empty:
            df[col] = df[col].fillna(df[col].mode()[0])

    return df


def sort_by_date(df, date_column):
    """
    Sort dataframe by date column.
    """

    if date_column:
        df = df.sort_values(by=date_column)

    return df


def detect_outliers(df):
    """
    Detect outliers using IQR.
    """

    outliers = {}

    numeric_columns = df.select_dtypes(include=["number"]).columns

    for col in numeric_columns:

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)

        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        count = ((df[col] < lower) | (df[col] > upper)).sum()

        outliers[col] = int(count)

    return outliers


def calculate_quality_score(df, duplicates_removed, outliers):

    score = 100

    missing = int(df.isnull().sum().sum())

    score -= missing

    score -= duplicates_removed

    score -= sum(outliers.values())

    if score < 0:
        score = 0

    return score


def generate_recommendations(score):

    recommendations = []

    if score >= 95:
        recommendations.append("Dataset is clean and ready for forecasting.")

    elif score >= 80:
        recommendations.append("Dataset is good. Minor preprocessing recommended.")

    else:
        recommendations.append("Dataset quality is low. Clean data before forecasting.")

    return recommendations


def preprocess_dataset(df, date_column):

    df, duplicates_removed = remove_duplicates(df)

    df = handle_missing_values(df)

    df = sort_by_date(df, date_column)

    outliers = detect_outliers(df)

    quality_score = calculate_quality_score(
        df,
        duplicates_removed,
        outliers
    )

    recommendations = generate_recommendations(
        quality_score
    )

    return {
        "processed_dataframe": df,
        "duplicates_removed": duplicates_removed,
        "quality_score": quality_score,
        "outliers": outliers,
        "recommendations": recommendations
    }