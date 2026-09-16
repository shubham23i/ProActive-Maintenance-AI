
import sys
import pandas as pd
import joblib

from xgboost import XGBClassifier

from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.exception.exception_handler import CustomException
from proactive_maintenance_ai.entity.config_entity import ModelTrainerConfig


class ModelTrainer:

    def __init__(self, config: ModelTrainerConfig):

        self.config = config

        self.target_column = self.config.target_column

        # Used only for chronological ordering
        self.order_column = "UDI"

    def load_data(self):

        try:

            train_df = pd.read_csv(
                self.config.input_train_data_file
            )

            test_df = pd.read_csv(
                self.config.input_test_data_file
            )

            logging.info(
                f"Train data loaded: {train_df.shape}"
            )

            logging.info(
                f"Test data loaded: {test_df.shape}"
            )

            return train_df, test_df

        except Exception as e:

            raise CustomException(e, sys)

    def prepare_features(self, df):

        try:

            df = df.copy()

            # ---------------------------------------------------------
            # Separate target
            # ---------------------------------------------------------

            y = df[self.target_column]

            # ---------------------------------------------------------
            # Remove target and UDI
            # ---------------------------------------------------------

            X = df.drop(
                columns=[
                    self.target_column,
                    self.order_column
                ],
                errors="ignore"
            )

            # ---------------------------------------------------------
            # Encode categorical column
            # ---------------------------------------------------------

            X = pd.get_dummies(
                X,
                columns=["Type"],
                drop_first=True,
                dtype=int
            )

            # ---------------------------------------------------------
            # Clean XGBoost feature names
            # ---------------------------------------------------------

            X.columns = (
                X.columns
                .str.replace("[", "_", regex=False)
                .str.replace("]", "_", regex=False)
                .str.replace("<", "_", regex=False)
                .str.replace(">", "_", regex=False)
                .str.replace(" ", "_", regex=False)
            )

            return X, y

        except Exception as e:

            raise CustomException(e, sys)

    def train_model(self):

        try:

            # ---------------------------------------------------------
            # Load data
            # ---------------------------------------------------------

            train_df, test_df = self.load_data()

            # ---------------------------------------------------------
            # Sort chronologically
            # ---------------------------------------------------------

            train_df = (
                train_df
                .sort_values(self.order_column)
                .reset_index(drop=True)
            )

            test_df = (
                test_df
                .sort_values(self.order_column)
                .reset_index(drop=True)
            )

            # ---------------------------------------------------------
            # Temporal validation split
            #
            # 85% -> model fitting
            # 15% -> validation
            #
            # Final test remains completely untouched.
            # ---------------------------------------------------------

            validation_size = int(
                len(train_df) * 0.15
            )

            if validation_size == 0:

                raise ValueError(
                    "Validation dataset is empty."
                )

            fit_df = train_df.iloc[
                :-validation_size
            ].copy()

            val_df = train_df.iloc[
                -validation_size:
            ].copy()

            logging.info(
                f"Fit data shape: {fit_df.shape}"
            )

            logging.info(
                f"Validation data shape: {val_df.shape}"
            )

            logging.info(
                f"Final test data shape: {test_df.shape}"
            )

            # ---------------------------------------------------------
            # Log temporal ranges
            # ---------------------------------------------------------

            logging.info(
                f"Fit UDI range: "
                f"{fit_df[self.order_column].min()} - "
                f"{fit_df[self.order_column].max()}"
            )

            logging.info(
                f"Validation UDI range: "
                f"{val_df[self.order_column].min()} - "
                f"{val_df[self.order_column].max()}"
            )

            logging.info(
                f"Test UDI range: "
                f"{test_df[self.order_column].min()} - "
                f"{test_df[self.order_column].max()}"
            )

            # ---------------------------------------------------------
            # Prepare features
            # ---------------------------------------------------------

            X_fit, y_fit = self.prepare_features(
                fit_df
            )

            X_val, y_val = self.prepare_features(
                val_df
            )

            X_test, y_test = self.prepare_features(
                test_df
            )

            # ---------------------------------------------------------
            # Align validation/test features with training features
            # ---------------------------------------------------------

            X_val = X_val.reindex(
                columns=X_fit.columns,
                fill_value=0
            )

            X_test = X_test.reindex(
                columns=X_fit.columns,
                fill_value=0
            )

            # ---------------------------------------------------------
            # Check target classes
            # ---------------------------------------------------------

            positive = (y_fit == 1).sum()
            negative = (y_fit == 0).sum()

            if positive == 0:

                raise ValueError(
                    "Training data contains no positive samples."
                )

            scale_pos_weight = (
                negative / positive
            )

            logging.info(
                f"Positive samples: {positive}"
            )

            logging.info(
                f"Negative samples: {negative}"
            )

            logging.info(
                f"Scale positive weight: "
                f"{scale_pos_weight:.2f}"
            )

            # ---------------------------------------------------------
            # XGBoost
            # ---------------------------------------------------------

            model = XGBClassifier(

                n_estimators=1000,

                max_depth=5,

                learning_rate=0.03,

                subsample=0.8,

                colsample_bytree=0.8,

                objective="binary:logistic",

                eval_metric="aucpr",

                scale_pos_weight=scale_pos_weight,

                random_state=42,

                n_jobs=-1,

                tree_method="hist",

                early_stopping_rounds=50
            )

            # ---------------------------------------------------------
            # Train
            # ---------------------------------------------------------

            logging.info(
                "Starting XGBoost training..."
            )

            model.fit(
                X_fit,
                y_fit,
                eval_set=[
                    (X_val, y_val)
                ],
                verbose=False
            )

            logging.info(
                "XGBoost training completed."
            )

            # ---------------------------------------------------------
            # Log best iteration
            # ---------------------------------------------------------

            if hasattr(
                model,
                "best_iteration"
            ):

                logging.info(
                    f"Best iteration: "
                    f"{model.best_iteration}"
                )

            # ---------------------------------------------------------
            # Save model
            # ---------------------------------------------------------

            joblib.dump(
                model,
                self.config.trained_model_path
            )

            logging.info(
                f"Model saved at: "
                f"{self.config.trained_model_path}"
            )

            return model

        except Exception as e:

            raise CustomException(e, sys)

    def initiate_model_training(self):

        try:

            logging.info("=" * 60)
            logging.info(
                "Model Training Started"
            )
            logging.info("=" * 60)

            model = self.train_model()

            logging.info(
                "Model Training Completed"
            )

            logging.info("=" * 60)

            return model

        except Exception as e:

            raise CustomException(e, sys)

