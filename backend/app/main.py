from fastapi import FastAPI
from app.api.upload import router as upload_router

app = FastAPI(
    title="Time Series Forecasting Suite",
    description="Backend API for Time Series Forecasting",
    version="1.0.0"
)

app.include_router(upload_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to Time Series Forecasting Suite!"
    }