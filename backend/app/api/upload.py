from fastapi import APIRouter, UploadFile, File
from app.services.analyze import analyze_dataset
from app.services.preprocess import preprocess_dataset
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

    # Return response
    return {
        "message": "File uploaded, analyzed and preprocessed successfully!",
        "filename": file.filename,
        "analysis": analysis,
        "preprocessing": {
            "duplicates_removed": preprocess_result["duplicates_removed"],
            "quality_score": preprocess_result["quality_score"],
            "outliers": preprocess_result["outliers"],
            "recommendations": preprocess_result["recommendations"]
        }
    }