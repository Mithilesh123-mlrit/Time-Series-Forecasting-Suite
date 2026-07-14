import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


def naive_forecast(df, target_column, forecast_steps=7):
    """
    Naive Forecast:
    Predict future values using the last observed value.
    """

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


def arima_forecast(df, target_column, forecast_steps=7):
    """
    ARIMA Forecast
    """

    try:
        series = df[target_column]

        model = ARIMA(series, order=(1, 1, 1))
        fitted_model = model.fit()

        forecast = fitted_model.forecast(steps=forecast_steps)

        return {
            "model": "ARIMA",
            "order": [1, 1, 1],
            "forecast_steps": forecast_steps,
            "forecast": forecast.tolist()
        }

    except Exception as e:
        return {
            "model": "ARIMA",
            "error": str(e)
        }