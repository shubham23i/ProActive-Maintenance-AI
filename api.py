from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from proactive_maintenance_ai.pipeline.prediction_pipeline import (
    PredictionPipeline
)


app = FastAPI(
    title="ProActive Maintenance AI",
    description="Predictive Maintenance and Machine Failure Risk API",
    version="1.0.0"
)


class PredictionRequest(BaseModel):

    Type: str
    Air_temperature_K: float
    Process_temperature_K: float
    Rotational_speed_rpm: float
    Torque_Nm: float
    Tool_wear_min: float


@app.get("/")
def root():

    return {
        "project": "ProActive Maintenance AI",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


pipeline = PredictionPipeline()


@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        input_data = {
            "Type": request.Type,
            "Air temperature [K]": request.Air_temperature_K,
            "Process temperature [K]": request.Process_temperature_K,
            "Rotational speed [rpm]": request.Rotational_speed_rpm,
            "Torque [Nm]": request.Torque_Nm,
            "Tool wear [min]": request.Tool_wear_min
        }

        return pipeline.start_prediction(input_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))