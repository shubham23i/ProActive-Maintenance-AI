import sys
import json
import joblib
import pandas as pd

from proactive_maintenance_ai.components.stage_10_maintenance_decision import (
    MaintenanceDecisionEngine
)
from proactive_maintenance_ai.components.stage_11_explainability import (
    ModelExplainability
)
from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.exception.exception_handler import CustomException
from proactive_maintenance_ai.components.stage_04_feature_engineering import (
    FeatureEngineering
)
from proactive_maintenance_ai.components.stage_09_anomaly_detection import (
    AnomalyDetection
)
from proactive_maintenance_ai.config.configuration import ConfigurationManager


class Prediction:

    def __init__(self, config):
        self.config = config

        anomaly_config = (
            ConfigurationManager()
            .get_anomaly_detection_config()
        )
        self.anomaly_detector = AnomalyDetection(anomaly_config)
        self.maintenance_engine = MaintenanceDecisionEngine()

        explainability_config = (
            ConfigurationManager()
            .get_explainability_config()
        )
        self.explainer = ModelExplainability(explainability_config)

    def load_model(self):
        try:
            logging.info("Loading registered model...")
            model = joblib.load(self.config.model_path)
            logging.info("Model loaded successfully.")
            return model
        except Exception as e:
            raise CustomException(e, sys)

    def check_input_distribution(self, input_data):
        try:
            ranges_path = "artifacts/model_training/input_ranges.json"

            with open(ranges_path, "r") as f:
                input_ranges = json.load(f)

            warnings = []

            for column, limits in input_ranges.items():
                value = input_data[column]

                if value < limits["min"] or value > limits["max"]:
                    warnings.append({
                        "feature": column,
                        "value": value,
                        "training_min": limits["min"],
                        "training_max": limits["max"],
                        "status": "OUT_OF_RANGE"
                    })

            return {
                "out_of_distribution": len(warnings) > 0,
                "distribution_warnings": warnings
            }

        except Exception as e:
            raise CustomException(e, sys)

    def create_prediction_row(self, input_data):
        try:
            required_columns = [
                "Type",
                "Air temperature [K]",
                "Process temperature [K]",
                "Rotational speed [rpm]",
                "Torque [Nm]",
                "Tool wear [min]"
            ]

            for column in required_columns:
                if column not in input_data:
                    raise ValueError(f"Missing prediction input: {column}")

            prediction_row = {
                "UDI": 1,
                "Product ID": "PREDICTION",
                "Type": input_data["Type"],
                "Air temperature [K]": input_data["Air temperature [K]"],
                "Process temperature [K]": input_data["Process temperature [K]"],
                "Rotational speed [rpm]": input_data["Rotational speed [rpm]"],
                "Torque [Nm]": input_data["Torque [Nm]"],
                "Tool wear [min]": input_data["Tool wear [min]"],
                "Machine failure": 0
            }

            return pd.DataFrame([prediction_row])

        except Exception as e:
            raise CustomException(e, sys)

    def preprocess_input(self, input_data):
        try:
            prediction_row = self.create_prediction_row(input_data)

            feature_engineering = FeatureEngineering(config=None)
            engineered_df = feature_engineering.create_features(prediction_row)

            if engineered_df.empty:
                raise ValueError("Feature engineering produced no data.")

            prediction_df = engineered_df.drop(
                columns=["Machine failure", "UDI", "Product ID"],
                errors="ignore"
            )

            prediction_df = pd.get_dummies(
                prediction_df,
                columns=["Type"],
                drop_first=True,
                dtype=int
            )

            prediction_df.columns = (
                prediction_df.columns
                .astype(str)
                .str.replace("[", "_", regex=False)
                .str.replace("]", "_", regex=False)
                .str.replace("<", "_", regex=False)
                .str.replace(">", "_", regex=False)
                .str.replace(" ", "_", regex=False)
            )

            return prediction_df, prediction_row

        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, input_data):
        try:
            model = self.load_model()

            df, _ = self.preprocess_input(input_data)
            distribution_check = self.check_input_distribution(input_data)

            if hasattr(model, "feature_names_in_"):
                df = df.reindex(
                    columns=model.feature_names_in_,
                    fill_value=0
                )

            prediction = model.predict(df)[0]
            probability = model.predict_proba(df)[0][1]

            if probability >= 0.70:
                risk = "HIGH"
            elif probability >= 0.40:
                risk = "MEDIUM"
            else:
                risk = "LOW"

            anomaly_result = self.anomaly_detector.predict(input_data)

            maintenance_result = self.maintenance_engine.generate_decision(
                risk_level=risk,
                anomaly_status=anomaly_result["anomaly_status"]
            )

            explanation = self.explainer.explain(input_data)

            result = {
                "prediction": int(prediction),
                "failure_probability": round(float(probability), 4),
                "risk_level": risk,
                "maintenance_priority": maintenance_result["maintenance_priority"],
                "recommended_action": maintenance_result["recommended_action"],
                "inspection_window": maintenance_result["inspection_window"],
                "anomaly_prediction": int(anomaly_result["anomaly_prediction"]),
                "anomaly_score": round(float(anomaly_result["anomaly_score"]), 4),
                "anomaly_status": anomaly_result["anomaly_status"],
                "out_of_distribution": distribution_check["out_of_distribution"],
                "distribution_warnings": distribution_check["distribution_warnings"],
                "top_risk_factors": explanation["top_risk_factors"]
            }

            return result

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_prediction(self, input_data):
        try:
            return self.predict(input_data)
        except Exception as e:
            raise CustomException(e, sys)
