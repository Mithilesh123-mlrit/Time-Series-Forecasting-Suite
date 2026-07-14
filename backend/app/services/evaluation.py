import numpy as np


def evaluate_forecast(actual, predicted):
    """
    Calculate MAE, RMSE and MAPE.
    """

    actual = np.array(actual)
    predicted = np.array(predicted)

    mae = np.mean(np.abs(actual - predicted))

    rmse = np.sqrt(np.mean((actual - predicted) ** 2))

    mape = np.mean(np.abs((actual - predicted) / actual)) * 100

    return {
        "MAE": round(float(mae), 2),
        "RMSE": round(float(rmse), 2),
        "MAPE": round(float(mape), 2)
    }