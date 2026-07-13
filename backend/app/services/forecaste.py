import pandas as pd


def naive_forecast(df, target_column, forecast_steps=7):
    """
    Naive Forecast:
    Predict future values using the last observed value.
    """

    # Last observed value
    last_value = df[target_column].iloc[-1]

    forecast = [float(last_value)] * forecast_steps

    return {
        "model": "Naive Forecast",
        "forecast_steps": forecast_steps,
        "forecast": forecast
    }