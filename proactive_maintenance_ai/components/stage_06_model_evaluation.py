import os
import sys
import joblib
import json
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay
)

from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.exception.exception_handler import CustomException


class ModelEvaluation:

    def __init__(self, config):
        self.config = config

    def load_model(self):

        try:

            logging.info("Loading trained model...")

            model = joblib.load(
                self.config.model_path
            )

            logging.info("Trained model loaded successfully.")

            return model

        except Exception as e:
            raise CustomException(e, sys)

    def load_test_data(self):

        try:

            logging.info("Loading test data...")

            test_df = pd.read_csv(
                self.config.test_data_path
            )

            target_column = self.config.target_column

            X_test = test_df.drop(
                columns=[target_column]
            )

            y_test = test_df[target_column]

            # Encode Type exactly as done during training
            X_test = pd.get_dummies(
                X_test,
                columns=["Type"],
                drop_first=True
            )

            # Clean feature names
            X_test.columns = (
                X_test.columns
                .str.replace("[", "_", regex=False)
                .str.replace("]", "_", regex=False)
                .str.replace("<", "_", regex=False)
                .str.replace(">", "_", regex=False)
                .str.replace(" ", "_")
            )

            logging.info(
                f"Test data shape: {X_test.shape}"
            )

            return X_test, y_test

        except Exception as e:
            raise CustomException(e, sys)

    def evaluate_model(self, model, X_test, y_test):

        try:

            logging.info("Starting model evaluation...")

            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]

            accuracy = accuracy_score(
                y_test,
                y_pred
            )

            precision = precision_score(
                y_test,
                y_pred,
                zero_division=0
            )

            recall = recall_score(
                y_test,
                y_pred,
                zero_division=0
            )

            f1 = f1_score(
                y_test,
                y_pred,
                zero_division=0
            )

            roc_auc = roc_auc_score(
                y_test,
                y_prob
            )

            pr_auc = average_precision_score(
                y_test,
                y_prob
            )

            metrics = {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "roc_auc": roc_auc,
                "pr_auc": pr_auc
            }

            logging.info(f"Accuracy: {accuracy:.4f}")
            logging.info(f"Precision: {precision:.4f}")
            logging.info(f"Recall: {recall:.4f}")
            logging.info(f"F1 Score: {f1:.4f}")
            logging.info(f"ROC-AUC: {roc_auc:.4f}")
            logging.info(f"PR-AUC: {pr_auc:.4f}")

            logging.info("\nClassification Report:")
            logging.info(
                f"\n{classification_report(y_test, y_pred)}"
            )

            return metrics, y_pred

        except Exception as e:
            raise CustomException(e, sys)

    def save_metrics(self, metrics):

        try:

            os.makedirs(
                self.config.root_dir,
                exist_ok=True
            )

            with open(
                self.config.metrics_file,
                "w"
            ) as f:

                json.dump(
                    metrics,
                    f,
                    indent=4
                )

            logging.info(
                f"Metrics saved to: "
                f"{self.config.metrics_file}"
            )

        except Exception as e:
            raise CustomException(e, sys)

    def save_confusion_matrix(
        self,
        y_test,
        y_pred
    ):

        try:

            os.makedirs(
                self.config.root_dir,
                exist_ok=True
            )

            cm = confusion_matrix(
                y_test,
                y_pred
            )

            disp = ConfusionMatrixDisplay(
                confusion_matrix=cm,
                display_labels=[
                    "No Failure",
                    "Failure"
                ]
            )

            disp.plot()

            plt.title(
                "Machine Failure Confusion Matrix"
            )

            plt.tight_layout()

            plt.savefig(
                self.config.confusion_matrix_path,
                dpi=150
            )

            plt.close()

            logging.info(
                f"Confusion matrix saved to: "
                f"{self.config.confusion_matrix_path}"
            )

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_evaluation(self):

        try:

            logging.info("=" * 60)
            logging.info("Model Evaluation Started")
            logging.info("=" * 60)

            model = self.load_model()

            X_test, y_test = self.load_test_data()

            metrics, y_pred = self.evaluate_model(
                model,
                X_test,
                y_test
            )

            self.save_metrics(
                metrics
            )

            self.save_confusion_matrix(
                y_test,
                y_pred
            )

            logging.info("=" * 60)
            logging.info("Model Evaluation Completed")
            logging.info("=" * 60)

            return metrics

        except Exception as e:
            raise CustomException(e, sys)