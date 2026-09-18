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

            logging.info(
                "Loading registered model..."
            )

            model = joblib.load(
                self.config.model_path
            )

            logging.info(
                "Model loaded successfully."
            )

            return model

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

                    raise ValueError(
                        f"Missing prediction input: {column}"
                    )

            prediction_row = {
                "UDI": 1,
                "Product ID": "PREDICTION",
                "Type": input_data["Type"],
                "Air temperature [K]":
                    input_data["Air temperature [K]"],
                "Process temperature [K]":
                    input_data["Process temperature [K]"],
                "Rotational speed [rpm]":
                    input_data["Rotational speed [rpm]"],
                "Torque [Nm]":
                    input_data["Torque [Nm]"],
                "Tool wear [min]":
                    input_data["Tool wear [min]"],
                "Machine failure": 0
            }

            return pd.DataFrame(
                [prediction_row]
            )

        except Exception as e:

            raise CustomException(e, sys)

    def preprocess_input(self, input_data):

        try:

            prediction_row = (
                self.create_prediction_row(
                    input_data
                )
            )

            logging.info(
                "Prediction raw row:"
            )

            logging.info(
                prediction_row.to_string()
            )

            feature_engineering = FeatureEngineering(
                config=None
            )

            engineered_df = (
                feature_engineering.create_features(
                    prediction_row
                )
            )

            if engineered_df.empty:

                raise ValueError(
                    "Feature engineering produced no data."
                )

            logging.info(
                "Engineered prediction row:"
            )

            logging.info(
                engineered_df.to_string()
            )

            prediction_df = engineered_df.drop(
                columns=[
                    "Machine failure",
                    "UDI",
                    "Product ID"
                ],
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
                f"Prediction preprocessing completed: "
                f"{prediction_df.shape}"
            )

            return (
                prediction_df,
                prediction_row,
                engineered_df
            )

        except Exception as e:

            raise CustomException(e, sys)

    def predict(self, input_data):

        try:

            model = self.load_model()

            (
                df,
                prediction_row,
                engineered_df
            ) = self.preprocess_input(
                input_data
            )

            if hasattr(
                model,
                "feature_names_in_"
            ):

                expected_features = (
                    model.feature_names_in_
                )

                df = df.reindex(
                    columns=expected_features,
                    fill_value=0
                )

            logging.info(
                f"MODEL EXPECTED FEATURES: "
                f"{len(model.feature_names_in_)}"
                if hasattr(
                    model,
                    "feature_names_in_"
                )
                else "Model has no feature_names_in_"
            )

            logging.info(
                f"PREDICTION FEATURES: "
                f"{len(df.columns)}"
            )

            logging.info(
                f"PREDICTION INPUT VALUES: "
                f"{df.iloc[0].to_dict()}"
            )

            prediction = (
                model.predict(df)[0]
            )

            probability = (
                model.predict_proba(df)[0][1]
            )

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

            explanation = (
                self.explainer.explain(
                    input_data
                )
            )

            selected_features = {}

            for column in [
                "Air_temperature__K_",
                "Process_temperature__K_",
                "Rotational_speed__rpm_",
                "Torque__Nm_",
                "Tool_wear__min_",
                "Temperature_Difference",
                "Mechanical_Power",
                "Torque_Speed_Ratio",
                "Tool_Wear_Risk",
                "Temperature_Stress",
                "Temperature_Torque_Interaction",
                "Speed_Torque_Interaction",
                "Wear_Power_Interaction"
            ]:

                if column in df.columns:

                    selected_features[column] = round(
                        float(df.iloc[0][column]),
                        4
                    )

            result = {

                "prediction": int(
                    prediction
                ),

                "failure_probability": round(
                    float(probability),
                    4
                ),

                "risk_level": risk,

                "maintenance_priority":
                    maintenance_result[
                        "maintenance_priority"
                    ],

                "recommended_action":
                    maintenance_result[
                        "recommended_action"
                    ],

                "inspection_window":
                    maintenance_result[
                        "inspection_window"
                    ],

                "anomaly_prediction":
                    anomaly_result[
                        "anomaly_prediction"
                    ],

                "anomaly_score":
                    anomaly_result[
                        "anomaly_score"
                    ],

                "anomaly_status":
                    anomaly_result[
                        "anomaly_status"
                    ],

                "top_risk_factors":
                    explanation[
                        "top_features"
                    ],

                "debug": {

                    "model_type":
                        type(model).__name__,

                    "input_shape":
                        list(df.shape),

                    "nonzero_features":
                        int(
                            (df.iloc[0] != 0).sum()
                        ),

                    "input_sum":
                        round(
                            float(df.iloc[0].sum()),
                            4
                        ),

                    "feature_count":
                        len(df.columns),

                    "selected_features":
                        selected_features,

                    "prediction_row_raw": {
                        k: (
                            None
                            if pd.isna(v)
                            else v
                        )
                        for k, v in
                        prediction_row.iloc[
                            0
                        ].to_dict().items()
                    },

                    "engineered_prediction_row": {
                        k: (
                            None
                            if pd.isna(v)
                            else v
                        )
                        for k, v in
                        engineered_df.iloc[
                            0
                        ].to_dict().items()
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

            logging.info(
                "=" * 60
            )

            logging.info(
                "PREDICTION STARTED"
            )

            logging.info(
                "=" * 60
            )

            result = self.predict(
                input_data
            )

            logging.info(
                "Prediction completed successfully."
            )

            logging.info(
                "=" * 60
            )

            return result

        except Exception as e:

            raise CustomException(e, sys)