import pandas as pd
import numpy as np
import sys

from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.entity.config_entity import FeatureEngineeringConfig
from proactive_maintenance_ai.exception.exception_handler import CustomException


class FeatureEngineering:

    def __init__(self, config: FeatureEngineeringConfig):
        self.config = config

        self.sensor_columns = [
            "Air temperature [K]",
            "Process temperature [K]",
            "Rotational speed [rpm]",
            "Torque [Nm]",
            "Tool wear [min]"
        ]

    def create_features(self, df):

        try:

            df = df.copy()

            # ---------------------------------------------------------
            # 1. Sort chronologically
            # ---------------------------------------------------------

            df = df.sort_values("UDI").reset_index(drop=True)

            features = {}

            # ---------------------------------------------------------
            # 2. Domain features
            # ---------------------------------------------------------

            features["Temperature Difference"] = (
                df["Process temperature [K]"]
                - df["Air temperature [K]"]
            )

            features["Mechanical Power"] = (
                df["Torque [Nm]"]
                * df["Rotational speed [rpm]"]
                * (2 * np.pi / 60)
            )

            features["Torque Speed Ratio"] = (
                df["Torque [Nm]"]
                / (df["Rotational speed [rpm]"] + 1e-6)
            )

            features["Tool Wear Risk"] = (
                df["Tool wear [min]"] / 250
            )

            features["Temperature Stress"] = (
                df["Air temperature [K]"]
                * df["Process temperature [K]"]
            )

            # ---------------------------------------------------------
            # 3. Interaction features
            # ---------------------------------------------------------

            features["Temperature_Torque_Interaction"] = (
                features["Temperature Difference"]
                * df["Torque [Nm]"]
            )

            features["Speed_Torque_Interaction"] = (
                df["Rotational speed [rpm]"]
                * df["Torque [Nm]"]
            )

            features["Wear_Power_Interaction"] = (
                df["Tool wear [min]"]
                * features["Mechanical Power"]
            )

            # ---------------------------------------------------------
            # 4. Add all features at once
            # ---------------------------------------------------------

            feature_df = pd.DataFrame(
                features,
                index=df.index
            )

            df = pd.concat(
                [df, feature_df],
                axis=1
            )

            # ---------------------------------------------------------
            # 5. Remove invalid rows
            # ---------------------------------------------------------

            df = df.replace(
                [np.inf, -np.inf],
                np.nan
            )

            if self.config is not None:
                df = df.dropna().reset_index(drop=True)
            else:
                df = df.reset_index(drop=True)

            # ---------------------------------------------------------
            # 6. Safety check
            # ---------------------------------------------------------

            if df.empty:
                raise ValueError(
                    "Feature engineering produced an empty dataset."
                )

            logging.info(
                f"Feature engineering completed. "
                f"Shape: {df.shape}"
            )

            logging.info(
                f"Features created: "
                f"{list(feature_df.columns)}"
            )

            return df

        except Exception as e:

            raise CustomException(e, sys)

    def save_data(self, train_df, test_df):

        try:

            train_df.to_csv(
                self.config.output_train_data_file,
                index=False
            )

            test_df.to_csv(
                self.config.output_test_data_file,
                index=False
            )

            logging.info(
                "Feature engineered train and test datasets saved."
            )

        except Exception as e:

            raise CustomException(e, sys)

    def initiate_feature_engineering(self):

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

            train_df = self.create_features(
                train_df
            )

            test_df = self.create_features(
                test_df
            )

            self.save_data(
                train_df,
                test_df
            )

            return train_df, test_df

        except Exception as e:

            raise CustomException(e, sys)