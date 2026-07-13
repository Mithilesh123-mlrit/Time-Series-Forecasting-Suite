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
def moving_average_forecast(df, target_column, forecast_steps=7, window=5):
    """
    Moving Average Forecast:
    Forecast using the average of the last 'window' observations.
    """

    recent_values = df[target_column].tail(window)

    average_value = recent_values.mean()

    forecast = [float(average_value)] * forecast_steps

    return {
        "model": "Moving Average",
        "window": window,
        "forecast_steps": forecast_steps,
        "forecast": forecast
    }