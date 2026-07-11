import pandas as pd


def detect_date_column(df):
    """
    Detect the most likely date column based on column names.
    """
    date_keywords = [
        "date",
        "time",
        "timestamp",
        "day",
        "month",
        "year"
    ]

    for column in df.columns:
        column_lower = column.lower()

        for keyword in date_keywords:
            if keyword in column_lower:
                return column

    return None


def detect_target_column(df):
    """
    Detect the best forecasting target column.
    """

    priority_columns = [
        "sales_amount",
        "revenue",
        "profit",
        "amount",
        "demand",
        "forecast",
        "quantity_sold",
        "quantity",
        "unit_price",
        "price",
        "sales"
    ]

    columns_lower = {col.lower(): col for col in df.columns}

    # Exact keyword match first
    for keyword in priority_columns:
        if keyword in columns_lower:
            return columns_lower[keyword]

    # Partial match
    for keyword in priority_columns:
        for column in df.columns:
            if keyword in column.lower():
                return column

    # First numeric column that is not an ID
    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()

    for column in numeric_columns:
        if "id" not in column.lower():
            return column

    return None

def analyze_dataset(file_path):
    """
    Read the dataset and generate an analysis report.
    """

    df = pd.read_csv(file_path)

    date_column = detect_date_column(df)

    # Convert detected date column into datetime format
    if date_column:
        df[date_column] = pd.to_datetime(df[date_column], errors="coerce")

    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()

    categorical_columns = df.select_dtypes(include=["object"]).columns.tolist()

    analysis = {
        "rows": len(df),
        "columns": len(df.columns),

        "column_names": list(df.columns),

        "data_types": df.dtypes.astype(str).to_dict(),

        "missing_values": df.isnull().sum().to_dict(),

        "duplicate_rows": int(df.duplicated().sum()),

        "numeric_columns": numeric_columns,

        "categorical_columns": categorical_columns,

        "date_column": date_column,

        "target_column": detect_target_column(df)
    }

    return analysis