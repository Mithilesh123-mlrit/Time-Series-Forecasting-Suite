from fastapi import APIRouter, UploadFile, File
from app.services.analyze import analyze_dataset
from app.services.preprocess import preprocess_dataset
from app.services.validation import validate_time_series
from app.services.feature_engineering import create_time_features
from app.services.train_test import train_test_split_time_series
from app.services.evaluation import evaluate_forecast
from app.services.forecaste import (
    naive_forecast,
    moving_average_forecast,
    arima_forecast
)

import pandas as pd
import os
import shutil

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Save uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Analyze dataset
    analysis = analyze_dataset(file_path)

    # Read dataset
    df = pd.read_csv(file_path)

    # Preprocess dataset
    preprocess_result = preprocess_dataset(
        df,
        analysis["date_column"]
    )

    # Validate time series
    validation_result = validate_time_series(
        df,
        analysis["date_column"],
        analysis["target_column"]
    )

    # Feature Engineering
    feature_result = create_time_features(
        df,
        analysis["date_column"]
    )

    # Train-Test Split
    split_result = train_test_split_time_series(
        df,
        analysis["target_column"],
        test_size=0.2
    )
    print("TRAIN TEST SPLIT:", split_result)

    train_df = split_result["train"]
    test_df = split_result["test"]

    # Forecasting Models
    forecast_result = naive_forecast(
        df,
        analysis["target_column"],
        forecast_steps=7
    )

    moving_average_result = moving_average_forecast(
        df,
        analysis["target_column"],
        forecast_steps=7,
        window=5
    )

    arima_result = arima_forecast(
        df,
        analysis["target_column"],
        forecast_steps=7
    )

    print("ARIMA RESULT:", arima_result)

    # Return Response
    return {
        "message": "File uploaded, analyzed, preprocessed, validated, feature engineered and forecasted successfully!",
        "filename": file.filename,

        "analysis": analysis,

        "preprocessing": {
            "duplicates_removed": preprocess_result["duplicates_removed"],
            "quality_score": preprocess_result["quality_score"],
            "outliers": preprocess_result["outliers"],
            "recommendations": preprocess_result["recommendations"]
        },

        "validation": validation_result,

        "feature_engineering": feature_result,

        "train_test_split": {
            "train_size": split_result["train_size"],
            "test_size": split_result["test_size"]
        },

        "forecast": {
            "naive_forecast": forecast_result,
            "moving_average_forecast": moving_average_result,
            "arima_forecast": arima_result
        }
    }