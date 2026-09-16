import sys
import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest

from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.exception.exception_handler import CustomException


class AnomalyDetection:

    def __init__(self, config):

        self.config = config

        self.feature_columns = [
            "Air temperature [K]",
            "Process temperature [K]",
            "Rotational speed [rpm]",
            "Torque [Nm]",
            "Tool wear [min]"
        ]

        self.model = IsolationForest(
            n_estimators=200,
            contamination=0.02,
            random_state=42,
            n_jobs=-1
        )

    def load_data(self):

        try:

            df = pd.read_csv(
                self.config.data_file
            )

            logging.info(
                f"Anomaly detection data loaded: {df.shape}"
            )

            return df

        except Exception as e:
            raise CustomException(e, sys)

    def train(self):

        try:

            df = self.load_data()

            X = df[
                self.feature_columns
            ].copy()

            X = X.dropna()

            logging.info(
                f"Training anomaly detector on: {X.shape}"
            )

            self.model.fit(X)

            joblib.dump(
                self.model,
                self.config.model_path
            )

            logging.info(
                f"Anomaly detection model saved: "
                f"{self.config.model_path}"
            )

            return self.model

        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, input_data):

        try:

            model = joblib.load(
                self.config.model_path
            )

            X = pd.DataFrame(
                [input_data]
            )

            X = X[
                self.feature_columns
            ]

            prediction = model.predict(X)[0]

            score = model.decision_function(X)[0]

            if prediction == -1:

                anomaly_status = "ANOMALY"

            else:

                anomaly_status = "NORMAL"

            result = {
                "anomaly_prediction": int(prediction),
                "anomaly_score": round(
                    float(score),
                    4
                ),
                "anomaly_status": anomaly_status
            }

            logging.info(
                f"Anomaly detection result: {result}"
            )

            return result

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_anomaly_detection(self):

        try:

            logging.info("=" * 60)
            logging.info("ANOMALY DETECTION STARTED")
            logging.info("=" * 60)

            model = self.train()

            logging.info(
                "Anomaly Detection Completed"
            )

            logging.info("=" * 60)

            return model

        except Exception as e:
            raise CustomException(e, sys)