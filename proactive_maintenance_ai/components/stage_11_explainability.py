import sys
import joblib
import pandas as pd
import shap

from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.exception.exception_handler import CustomException


class ModelExplainability:

    def __init__(self, config):

        self.config = config

    def load_model(self):

        try:

            logging.info("Loading model for explainability...")

            model = joblib.load(
                self.config.model_path
            )

            logging.info(
                "Model loaded successfully."
            )

            return model

        except Exception as e:
            raise CustomException(e, sys)

    def explain(self, input_data):

        try:

            model = self.load_model()

            X = pd.DataFrame(
                [input_data]
            )

            X = pd.get_dummies(
                X,
                columns=["Type"],
                drop_first=True,
                dtype=int
            )

            X.columns = (
                X.columns
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

            if hasattr(model, "feature_names_in_"):

                expected_features = (
                    model.feature_names_in_
                )

                X = X.reindex(
                    columns=expected_features,
                    fill_value=0
                )

            explainer = shap.TreeExplainer(
                model
            )

            shap_values = explainer.shap_values(
                X
            )

            if isinstance(shap_values, list):
                shap_values = shap_values[0]

            shap_values = shap_values[0]

            feature_importance = []

            for feature, value in zip(
                X.columns,
                shap_values
            ):

                feature_importance.append(
                    {
                        "feature": feature,
                        "impact": round(
                            float(value),
                            4
                        ),
                        "direction": (
                            "INCREASES RISK"
                            if value > 0
                            else "DECREASES RISK"
                        )
                    }
                )

            feature_importance = sorted(
                feature_importance,
                key=lambda x: abs(
                    x["impact"]
                ),
                reverse=True
            )

            result = {
                "top_features": feature_importance[:5]
            }

            logging.info(
                f"Explainability result: {result}"
            )

            return result

        except Exception as e:
            raise CustomException(e, sys)