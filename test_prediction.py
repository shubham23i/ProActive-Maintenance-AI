from proactive_maintenance_ai.pipeline.prediction_pipeline import PredictionPipeline


input_data = {
    "Type": "M",
    "Air temperature [K]": 300.0,
    "Process temperature [K]": 310.0,
    "Rotational speed [rpm]": 1500,
    "Torque [Nm]": 40.0,
    "Tool wear [min]": 100
}


pipeline = PredictionPipeline()

result = pipeline.start_prediction(input_data)

print(result)