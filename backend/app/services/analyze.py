import pandas as pd


def analyze_dataset(file_path):
    df = pd.read_csv(file_path)

    analysis = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict()
    }

    return analysis