import pandas as pd


def train_test_split_time_series(df, target_column, test_size=0.2):
    """
    Split a time series dataset into training and testing sets.
    """

    split_index = int(len(df) * (1 - test_size))

    train = df.iloc[:split_index]
    test = df.iloc[split_index:]

    return {
        "train": train,
        "test": test,
        "train_size": len(train),
        "test_size": len(test)
    }