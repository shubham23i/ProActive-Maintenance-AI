import sys
import joblib
import pandas as pd

from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.exception.exception_handler import CustomException


class Prediction:

    def __init__(self, config):
        self.config = config

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

    def preprocess_input(self, input_data):

        try:

            df = pd.DataFrame([input_data])

            # Remove UDI if supplied
            if "UDI" in df.columns:
                df = df.drop(columns=["UDI"])

            # Remove Product ID if supplied
            if "Product ID" in df.columns:
                df = df.drop(columns=["Product ID"])

            # Encode Type
            df = pd.get_dummies(
                df,
                columns=["Type"],
                drop_first=True
            )

            # Clean feature names
            df.columns = (
                df.columns
                .astype(str)
                .str.replace("[", "_", regex=False)
                .str.replace("]", "_", regex=False)
                .str.replace("<", "_", regex=False)
                .str.replace(">", "_", regex=False)
                .str.replace(" ", "_", regex=False)
            )

            logging.info(
                f"Input preprocessing completed: {df.shape}"
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

            # Match training features
            if hasattr(model, "feature_names_in_"):

                expected_features = (
                    model.feature_names_in_
                )

                df = df.reindex(
                    columns=expected_features,
                    fill_value=0
                )

            prediction = model.predict(df)[0]

            probability = model.predict_proba(
                df
            )[0][1]

            if probability >= 0.70:
                risk = "HIGH"

            elif probability >= 0.40:
                risk = "MEDIUM"

            else:
                risk = "LOW"

            result = {
                "prediction": int(prediction),
                "failure_probability": round(
                    float(probability),
                    4
                ),
                "risk_level": risk
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