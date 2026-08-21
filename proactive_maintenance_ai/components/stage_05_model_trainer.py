import os
import sys
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.exception.exception_handler import CustomException


class ModelTrainer:

    def __init__(self, config):
        self.config = config

    def load_data(self):

        try:

            logging.info("Loading feature engineered data...")

            train_df = pd.read_csv(
                self.config.input_train_data_file
            )

            test_df = pd.read_csv(
                self.config.input_test_data_file
            )

            logging.info(
                f"Training data shape: {train_df.shape}"
            )

            logging.info(
                f"Testing data shape: {test_df.shape}"
            )

            return train_df, test_df

        except Exception as e:
            raise CustomException(e, sys)

    def train_model(self, X_train, y_train):

        try:

            logging.info("Starting XGBoost model training...")

            # Handle class imbalance
            negative_count = (y_train == 0).sum()
            positive_count = (y_train == 1).sum()

            scale_pos_weight = (
                negative_count / positive_count
                if positive_count > 0
                else 1
            )

            logging.info(
                f"Scale positive weight: {scale_pos_weight}"
            )

            model = XGBClassifier(
                n_estimators=300,
                max_depth=6,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                objective="binary:logistic",
                eval_metric="logloss",
                scale_pos_weight=scale_pos_weight,
                random_state=42,
                n_jobs=-1
            )

            model.fit(
                X_train,
                y_train
            )

            logging.info(
                "XGBoost model training completed."
            )

            return model

        except Exception as e:
            raise CustomException(e, sys)

    def save_model(self, model):

        try:

            os.makedirs(
                self.config.root_dir,
                exist_ok=True
            )

            joblib.dump(
                model,
                self.config.trained_model_path
            )

            logging.info(
                f"Model saved successfully to: "
                f"{self.config.trained_model_path}"
            )

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_training(self):

        try:

            logging.info("=" * 60)
            logging.info("Model Training Started")
            logging.info("=" * 60)

            train_df, test_df = self.load_data()

            target_column = self.config.target_column

            # Separate features and target
            X = train_df.drop(columns=[target_column])
            y = train_df[target_column]

            
            

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42,
                stratify=y
            )

            # Encode categorical column
            X_train = pd.get_dummies(
                X_train,
                columns=["Type"],
                drop_first=True
            )

            X_test = pd.get_dummies(
                X_test,
                columns=["Type"],
                drop_first=True
            )

            # Make sure train and test have identical columns
            X_train, X_test = X_train.align(
                X_test,
                join="left",
                axis=1,
                fill_value=0
            )
            # Clean feature names for XGBoost
            X_train.columns = (
                X_train.columns
                .str.replace("[", "_", regex=False)
                .str.replace("]", "_", regex=False)
                .str.replace("<", "_", regex=False)
                .str.replace(">", "_", regex=False)
                .str.replace(" ", "_")
            )

            X_test.columns = X_train.columns

            logging.info(
                f"Training features: {X_train.shape}"
            )

            logging.info(
                f"Testing features: {X_test.shape}"
            )

            # Train model
            model = self.train_model(
                X_train,
                y_train
            )

            # Save model
            self.save_model(model)

            logging.info("=" * 60)
            logging.info("Model Training Completed")
            logging.info("=" * 60)

            return model, X_test, y_test

        except Exception as e:
            raise CustomException(e, sys)