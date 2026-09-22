import pandas as pd
import joblib
import json
import sys
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    brier_score_loss
)

from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.entity.config_entity import ModelEvaluationConfig
from proactive_maintenance_ai.exception.exception_handler import CustomException


class ModelEvaluation:

    def __init__(self, config: ModelEvaluationConfig):

        self.config = config
        self.target_column = "Machine failure"

    def evaluate(self):

        try:

            model = joblib.load(
                self.config.model_path
            )

            test_df = pd.read_csv(
                self.config.test_data_path
            )

            logging.info(
                f"Raw test data loaded: {test_df.shape}"
            )

            y_test = test_df[
                self.target_column
            ]

            X_test = test_df.drop(
                columns=[
                    self.target_column,
                    "UDI",
                    "Product ID"
                ],
                errors="ignore"
            )

            X_test = pd.get_dummies(
                X_test,
                columns=["Type"],
                drop_first=True,
                dtype=int
            )

            X_test.columns = (
                X_test.columns
                .str.replace("[", "_", regex=False)
                .str.replace("]", "_", regex=False)
                .str.replace("<", "_", regex=False)
                .str.replace(">", "_", regex=False)
                .str.replace(" ", "_", regex=False)
            )

            if hasattr(model, "feature_names_in_"):

                X_test = X_test.reindex(
                    columns=model.feature_names_in_,
                    fill_value=0
                )

            logging.info(
                f"Final evaluation feature shape: {X_test.shape}"
            )

            y_pred = model.predict(
                X_test
            )

            y_prob = model.predict_proba(
                X_test
            )[:, 1]

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
                ),

                "brier_score": brier_score_loss(
                    y_test,
                    y_prob
                )
            }

            metrics["actual_failure_rate"] = float(
                y_test.mean()
            )

            metrics["predicted_failure_rate"] = float(
                y_pred.mean()
            )

            metrics["mean_predicted_probability"] = float(
                y_prob.mean()
            )

            metrics["min_predicted_probability"] = float(
                y_prob.min()
            )

            metrics["max_predicted_probability"] = float(
                y_prob.max()
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

            plt.xticks(
                [0, 1],
                ["No Failure", "Failure"]
            )

            plt.yticks(
                [0, 1],
                ["No Failure", "Failure"]
            )

            for i in range(cm.shape[0]):
                for j in range(cm.shape[1]):
                    plt.text(
                        j,
                        i,
                        cm[i, j],
                        ha="center",
                        va="center"
                    )

            plt.savefig(
                self.config.confusion_matrix_path,
                dpi=300,
                bbox_inches="tight"
            )

            plt.close()

            return metrics

        except Exception as e:

            raise CustomException(e, sys)

    def initiate_model_evaluation(self):

        try:

            logging.info(
                "Model Evaluation Started"
            )

            metrics = self.evaluate()

            logging.info(
                "Model Evaluation Completed"
            )

            return metrics

        except Exception as e:

            raise CustomException(e, sys)