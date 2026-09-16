import pandas as pd
import joblib
import json
import sys
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix
)

import matplotlib.pyplot as plt

from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.entity.config_entity import ModelEvaluationConfig
from proactive_maintenance_ai.exception.exception_handler import CustomException


class ModelEvaluation:

    def __init__(self, config: ModelEvaluationConfig):

        self.config = config

        self.target_column = "Machine failure"

    def evaluate(self):

        try:

            # ---------------------------------------------------------
            # Load model
            # ---------------------------------------------------------

            model = joblib.load(
                self.config.model_path
            )

            # ---------------------------------------------------------
            # Load test data
            # ---------------------------------------------------------

            test_df = pd.read_csv(
                self.config.test_data_path
            )

            # ---------------------------------------------------------
            # Prepare X and y
            # ---------------------------------------------------------

            X_test = test_df.drop(
                columns=[
                    self.target_column,
                    "UDI"
                ],
                errors="ignore"
            )

            y_test = test_df[
                self.target_column
            ]

            # ---------------------------------------------------------
            # Encode categorical variables
            # ---------------------------------------------------------

            X_test = pd.get_dummies(
                X_test,
                columns=["Type"],
                drop_first=True,
                dtype=int
            )

            # ---------------------------------------------------------
            # Clean feature names
            # ---------------------------------------------------------

            X_test.columns = (
                X_test.columns
                .str.replace("[", "_", regex=False)
                .str.replace("]", "_", regex=False)
                .str.replace("<", "_", regex=False)
                .str.replace(">", "_", regex=False)
                .str.replace(" ", "_", regex=False)
            )

            # ---------------------------------------------------------
            # Match training feature schema
            # ---------------------------------------------------------

            if hasattr(model, "feature_names_in_"):

                X_test = X_test.reindex(
                    columns=model.feature_names_in_,
                    fill_value=0
                )

            # ---------------------------------------------------------
            # Predictions
            # ---------------------------------------------------------

            y_pred = model.predict(
                X_test
            )

            y_prob = model.predict_proba(
                X_test
            )[:, 1]

            # ---------------------------------------------------------
            # Metrics
            # ---------------------------------------------------------

            metrics = {

                "accuracy": accuracy_score(
                    y_test,
                    y_pred
                ),

                "precision": precision_score(
                    y_test,
                    y_pred,
                    zero_division=0
                ),

                "recall": recall_score(
                    y_test,
                    y_pred,
                    zero_division=0
                ),

                "f1_score": f1_score(
                    y_test,
                    y_pred,
                    zero_division=0
                ),

                "roc_auc": roc_auc_score(
                    y_test,
                    y_prob
                ),

                "pr_auc": average_precision_score(
                    y_test,
                    y_prob
                )
            }

            # ---------------------------------------------------------
            # Save metrics
            # ---------------------------------------------------------

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
                f"Evaluation metrics: {metrics}"
            )

            # ---------------------------------------------------------
            # Confusion matrix
            # ---------------------------------------------------------

            cm = confusion_matrix(
                y_test,
                y_pred
            )

            plt.figure(
                figsize=(6, 5)
            )

            plt.imshow(cm)

            plt.title(
                "Confusion Matrix"
            )

            plt.xlabel(
                "Predicted"
            )

            plt.ylabel(
                "Actual"
            )

            plt.colorbar()

            plt.savefig(
                self.config.confusion_matrix_path,
                dpi=300,
                bbox_inches="tight"
            )

            plt.close()

            return metrics

        except Exception as e:

            raise CustomException(e,sys)

    def initiate_model_evaluation(self):

        try:

            logging.info("=" * 60)
            logging.info("Model Evaluation Started")
            logging.info("=" * 60)

            metrics = self.evaluate()

            logging.info(
                "Model Evaluation Completed"
            )

            logging.info("=" * 60)

            return metrics

        except Exception as e:

            raise CustomException(e, sys)