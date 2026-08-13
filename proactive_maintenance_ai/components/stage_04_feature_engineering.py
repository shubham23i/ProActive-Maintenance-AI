import os
import sys
import pandas as pd
import numpy as np

from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.exception.exception_handler import CustomException


class FeatureEngineering:

    def __init__(self, config):
        self.config = config

    def load_data(self):
        try:

            logging.info("Loading preprocessed training and testing data...")

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

    def create_features(self, df):

        try:

            logging.info("Creating engineered features...")

            df = df.copy()

            # ------------------------------------------------
            # 1. Temperature Difference
            # ------------------------------------------------

            df["Temperature Difference [K]"] = (
                df["Process temperature [K]"]
                - df["Air temperature [K]"]
            )

            # ------------------------------------------------
            # 2. Mechanical Power Approximation
            # ------------------------------------------------
            # Power is proportional to:
            # Torque × Angular Velocity
            #
            # Since RPM is used instead of angular velocity,
            # this is used as a relative power/load indicator.

            df["Mechanical Power"] = (
                df["Torque [Nm]"]
                * df["Rotational speed [rpm]"]
            )

            # ------------------------------------------------
            # 3. Torque-Speed Ratio
            # ------------------------------------------------

            df["Torque-Speed Ratio"] = (
                df["Torque [Nm]"]
                / df["Rotational speed [rpm]"].replace(0, np.nan)
            )

            df["Torque-Speed Ratio"] = (
                df["Torque-Speed Ratio"].fillna(0)
            )

            # ------------------------------------------------
            # 4. Tool Wear Risk
            # ------------------------------------------------

            df["Tool Wear Risk"] = (
                df["Tool wear [min]"] / 250
            )

            # ------------------------------------------------
            # 5. Temperature Stress
            # ------------------------------------------------

            df["Temperature Stress"] = (
                df["Process temperature [K]"]
                * df["Torque [Nm]"]
            )

            logging.info(
                "Feature engineering completed."
            )

            return df

        except Exception as e:
            raise CustomException(e, sys)

    def save_data(self, train_df, test_df):

        try:

            os.makedirs(
                self.config.root_dir,
                exist_ok=True
            )

            train_df.to_csv(
                self.config.output_train_data_file,
                index=False
            )

            test_df.to_csv(
                self.config.output_test_data_file,
                index=False
            )

            logging.info(
                "Feature engineered datasets saved successfully."
            )

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_feature_engineering(self):

        try:

            logging.info("=" * 60)
            logging.info("Feature Engineering Started")
            logging.info("=" * 60)

            train_df, test_df = self.load_data()

            train_df = self.create_features(train_df)

            test_df = self.create_features(test_df)

            self.save_data(
                train_df,
                test_df
            )

            logging.info("=" * 60)
            logging.info(
                "Feature Engineering Completed Successfully"
            )
            logging.info("=" * 60)

            return train_df, test_df

        except Exception as e:
            raise CustomException(e, sys)

    def save_data(self, train_df, test_df):

        try:

            # Create feature engineering output directory
            os.makedirs(
                self.config.root_dir,
                exist_ok=True
            )

            # Save engineered training data
            train_df.to_csv(
                self.config.output_train_data_file,
                index=False
            )

            # Save engineered testing data
            test_df.to_csv(
                self.config.output_test_data_file,
                index=False
            )

            logging.info(
                f"Feature engineered training data saved to: "
                f"{self.config.output_train_data_file}"
            )

            logging.info(
                f"Feature engineered testing data saved to: "
                f"{self.config.output_test_data_file}"
            )

        except Exception as e:
            raise CustomException(e, sys)