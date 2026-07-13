from fastapi import APIRouter, UploadFile, File
from app.services.analyze import analyze_dataset
from app.services.preprocess import preprocess_dataset
from app.services.validation import validate_time_series
from app.services.feature_engineering import create_time_features
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

    feature_result = create_time_features(
    df,
    analysis["date_column"]
)

    # Return response
    return {
    "message": "File uploaded, analyzed, preprocessed, validated and feature engineered successfully!",
    "filename": file.filename,

    "analysis": analysis,

    "preprocessing": {
        "duplicates_removed": preprocess_result["duplicates_removed"],
        "quality_score": preprocess_result["quality_score"],
        "outliers": preprocess_result["outliers"],
        "recommendations": preprocess_result["recommendations"]
    },

    "validation": validation_result,

    "feature_engineering": feature_result
}