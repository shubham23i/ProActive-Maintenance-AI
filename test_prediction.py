from proactive_maintenance_ai.pipeline.prediction_pipeline import PredictionPipeline

input_data = {
    "Type": "M",
    "Air temperature [K]": 298.1,
    "Process temperature [K]": 308.6,
    "Rotational speed [rpm]": 1550,
    "Torque [Nm]": 42.5,
    "Tool wear [min]": 180
}

pipeline = PredictionPipeline()

result = pipeline.start_prediction(input_data)

print(result)