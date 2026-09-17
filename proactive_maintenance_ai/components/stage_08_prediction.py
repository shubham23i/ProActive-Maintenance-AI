import sys
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
from proactive_maintenance_ai.components.stage_04_feature_engineering import FeatureEngineering
from proactive_maintenance_ai.components.stage_09_anomaly_detection import AnomalyDetection
from proactive_maintenance_ai.config.configuration import ConfigurationManager


class Prediction:

    def __init__(self, config):
        self.config = config

        anomaly_config = (
            ConfigurationManager()
            .get_anomaly_detection_config()
        )

        self.anomaly_detector = AnomalyDetection(
            anomaly_config
        )
        self.maintenance_engine = MaintenanceDecisionEngine()
        explainability_config = (
            ConfigurationManager()
            .get_explainability_config()
        )

        self.explainer = ModelExplainability(
            explainability_config
        )

    def load_model(self):

        try:

            logging.info("Loading registered model...")

            model = joblib.load(
                self.config.model_path
            )

            logging.info("Model loaded successfully.")

            return model

        except Exception as e:
            raise CustomException(e, sys)

    def load_historical_data(self):

        try:

            df = pd.read_csv(
                self.config.raw_data_file
            )

            if df.empty:
                raise ValueError(
                    "Historical dataset is empty."
                )

            df = df.sort_values(
                "UDI"
            ).reset_index(drop=True)

            logging.info(
                f"Historical data loaded: {df.shape}"
            )

            return df

        except Exception as e:
            raise CustomException(e, sys)

    def create_prediction_row(self, input_data, historical_df):

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
                    raise ValueError(
                        f"Missing prediction input: {column}"
                    )

            next_udi = (
                int(historical_df["UDI"].max()) + 1
            )

            prediction_row = {
                "UDI": next_udi,
                "Product ID": "PREDICTION",
                "Type": input_data["Type"],
                "Air temperature [K]": input_data[
                    "Air temperature [K]"
                ],
                "Process temperature [K]": input_data[
                    "Process temperature [K]"
                ],
                "Rotational speed [rpm]": input_data[
                    "Rotational speed [rpm]"
                ],
                "Torque [Nm]": input_data[
                    "Torque [Nm]"
                ],
                "Tool wear [min]": input_data[
                    "Tool wear [min]"
                ]
            }

            return pd.DataFrame([prediction_row])

        except Exception as e:
            raise CustomException(e, sys)

    def preprocess_input(self, input_data):

        try:

            historical_df = self.load_historical_data()

            prediction_row = self.create_prediction_row(
                input_data,
                historical_df
            )

            historical_context = historical_df.tail(30).copy()

            combined_df = pd.concat(
                [
                    historical_context,
                    prediction_row
                ],
                ignore_index=True
            )

            feature_engineering = FeatureEngineering(
                config=None
            )

            engineered_df = feature_engineering.create_features(
                combined_df
            )

            if engineered_df.empty:
                raise ValueError(
                    "Feature engineering produced no data."
                )

            df = engineered_df.tail(1).copy()

            df = df.drop(
                columns=["Machine failure"],
                errors="ignore"
            )

            df = df.drop(
                columns=["UDI", "Product ID"],
                errors="ignore"
            )

            df = pd.get_dummies(
                df,
                columns=["Type"],
                drop_first=True,
                dtype=int
            )

            df.columns = (
                df.columns.astype(str)
                .str.replace(
                    "[", "_", regex=False
                )
                .str.replace(
                    "]", "_", regex=False
                )
                .str.replace(
                    "<", "_", regex=False
                )
                .str.replace(
                    ">", "_", regex=False
                )
                .str.replace(
                    " ", "_", regex=False
                )
            )

            logging.info(
                f"Prediction preprocessing completed: {df.shape}"
            )

            return df

        except Exception as e:

            raise CustomException(e, sys)

    def predict(self, input_data):

        try:

            model = self.load_model()

            df = self.preprocess_input(
                input_data
            )

            if hasattr(model, "feature_names_in_"):

                expected_features = (
                    model.feature_names_in_
                )

                df = df.reindex(
                    columns=expected_features,
                    fill_value=0
                )
                debug_values = {
                    column: float(df.iloc[0][column])
                    for column in df.columns
                    if float(df.iloc[0][column]) != 0
                }

                result_debug = {
                    "input_sum": round(float(df.iloc[0].sum()), 4),
                    "nonzero_features": int((df.iloc[0] != 0).sum()),
                    "selected_features": {
                        column: round(float(df.iloc[0][column]), 4)
                        for column in [
                            "Air_temperature__K_",
                            "Process_temperature__K_",
                            "Rotational_speed__rpm_",
                            "Torque__Nm_",
                            "Tool_wear__min_",
                            "Temperature_Difference",
                            "Mechanical_Power",
                            "Speed_Torque_Interaction"
                        ]
                        if column in df.columns
                    }
                }

            prediction = model.predict(df)[0]
            probability = model.predict_proba(df)[0][1]

            logging.info(f"MODEL TYPE: {type(model)}")
            logging.info(f"INPUT SHAPE: {df.shape}")
            logging.info(f"INPUT SUM: {df.iloc[0].sum()}")
            logging.info(f"INPUT NONZERO: {(df.iloc[0] != 0).sum()}")
            logging.info(f"PROBABILITY: {probability}")

            if probability >= 0.70:

                risk = "HIGH"

            elif probability >= 0.40:

                risk = "MEDIUM"

            else:

                risk = "LOW"

            anomaly_result = (
                self.anomaly_detector.predict(
                    input_data
                )
            )

            maintenance_result = (
                self.maintenance_engine.generate_decision(
                    risk_level=risk,
                    anomaly_status=anomaly_result[
                        "anomaly_status"
                    ]
                )
            )
            explanation = self.explainer.explain(
                input_data
            )

            result = {
                "prediction": int(prediction),
                "failure_probability": round(float(probability), 4),
                "risk_level": risk,

                "maintenance_priority": maintenance_result["maintenance_priority"],
                "recommended_action": maintenance_result["recommended_action"],
                "inspection_window": maintenance_result["inspection_window"],

                "anomaly_prediction": anomaly_result["anomaly_prediction"],
                "anomaly_score": anomaly_result["anomaly_score"],
                "anomaly_status": anomaly_result["anomaly_status"],

                "top_risk_factors": explanation["top_features"],

                "debug": {
                    "model_type": type(model).__name__,
                    "input_shape": list(df.shape),
                    "nonzero_features": int((df.iloc[0] != 0).sum()),
                    "input_sum": round(float(df.iloc[0].sum()), 4),
                    "feature_count": len(df.columns),
                    "selected_features": {
                        column: round(float(df.iloc[0][column]), 4)
                        for column in [
                            "Air_temperature__K_",
                            "Process_temperature__K_",
                            "Rotational_speed__rpm_",
                            "Torque__Nm_",
                            "Tool_wear__min_",
                            "Temperature_Difference",
                            "Mechanical_Power",
                            "Speed_Torque_Interaction"
                        ]
                        if column in df.columns
                    }
                }
            }

            logging.info(
                f"Prediction result: {result}"
            )

            return result

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_prediction(self, input_data):

        try:

            logging.info("=" * 60)
            logging.info("PREDICTION STARTED")
            logging.info("=" * 60)

            result = self.predict(
                input_data
            )

            logging.info(
                "Prediction completed successfully."
            )

            logging.info("=" * 60)

            return result

        except Exception as e:
            raise CustomException(e, sys)