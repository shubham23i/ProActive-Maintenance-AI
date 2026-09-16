from proactive_maintenance_ai.config.configuration import ConfigurationManager
from proactive_maintenance_ai.components.stage_09_anomaly_detection import AnomalyDetection


config = ConfigurationManager()

anomaly_config = config.get_anomaly_detection_config()

anomaly_detector = AnomalyDetection(
    config=anomaly_config
)

input_data = {
    "Air temperature [K]": 298.5,
    "Process temperature [K]": 308.7,
    "Rotational speed [rpm]": 1500,
    "Torque [Nm]": 40.0,
    "Tool wear [min]": 100
}

result = anomaly_detector.predict(input_data)

print(result)