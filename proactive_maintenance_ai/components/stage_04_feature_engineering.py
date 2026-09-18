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
            # 2. Existing domain features
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
            # 3. Lag features
            # ---------------------------------------------------------

            for column in self.sensor_columns:

                for lag in [1, 3, 5, 10]:

                    features[f"{column}_lag_{lag}"] = (
                        df[column].shift(lag)
                    )

            # ---------------------------------------------------------
            # 4. Rolling statistics
            # ---------------------------------------------------------

            for column in self.sensor_columns:

                historical = df[column].shift(1)

                for window in [5, 10, 20]:

                    rolling = historical.rolling(window)

                    features[
                        f"{column}_rolling_mean_{window}"
                    ] = rolling.mean()

                    features[
                        f"{column}_rolling_std_{window}"
                    ] = rolling.std()

                    features[
                        f"{column}_rolling_min_{window}"
                    ] = rolling.min()

                    features[
                        f"{column}_rolling_max_{window}"
                    ] = rolling.max()

            # ---------------------------------------------------------
            # 5. Delta features
            # ---------------------------------------------------------

            for column in self.sensor_columns:

                features[f"{column}_delta_1"] = (
                    df[column] - df[column].shift(1)
                )

                features[f"{column}_delta_5"] = (
                    df[column] - df[column].shift(5)
                )

            # ---------------------------------------------------------
            # 6. Percentage change
            # ---------------------------------------------------------

            for column in self.sensor_columns:

                features[f"{column}_pct_change"] = (
                    df[column]
                    .pct_change()
                    .replace([np.inf, -np.inf], np.nan)
                )

            # ---------------------------------------------------------
            # 7. Rolling trend / degradation slope
            # ---------------------------------------------------------

            def rolling_slope(series, window):

                x = np.arange(window)

                return series.rolling(window).apply(
                    lambda y: np.polyfit(x, y, 1)[0]
                    if np.isfinite(y).all()
                    else np.nan,
                    raw=True
                )

            trend_columns = [
                "Torque [Nm]",
                "Rotational speed [rpm]",
                "Tool wear [min]"
            ]

            # Temperature Difference is created above,
            # so calculate it separately for trend features.
            temperature_difference = (
                df["Process temperature [K]"]
                - df["Air temperature [K]"]
            )

            trend_data = {
                "Torque [Nm]": df["Torque [Nm]"],
                "Rotational speed [rpm]": df["Rotational speed [rpm]"],
                "Tool wear [min]": df["Tool wear [min]"],
                "Temperature Difference": temperature_difference
            }

            for column in trend_columns + ["Temperature Difference"]:

                historical = trend_data[column].shift(1)

                for window in [10, 20]:

                    features[
                        f"{column}_trend_{window}"
                    ] = rolling_slope(
                        historical,
                        window
                    )

            # ---------------------------------------------------------
            # 8. Interaction features
            # ---------------------------------------------------------

            features["Temperature_Torque_Interaction"] = (
                (
                    df["Process temperature [K]"]
                    - df["Air temperature [K]"]
                )
                * df["Torque [Nm]"]
            )

            features["Speed_Torque_Interaction"] = (
                df["Rotational speed [rpm]"]
                * df["Torque [Nm]"]
            )

            mechanical_power = (
                df["Torque [Nm]"]
                * df["Rotational speed [rpm]"]
                * (2 * np.pi / 60)
            )

            features["Wear_Power_Interaction"] = (
                df["Tool wear [min]"]
                * mechanical_power
            )

            # ---------------------------------------------------------
            # 9. Add all features at once
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
            # 10. Remove unavailable historical rows
            # ---------------------------------------------------------

            if self.config is not None:
                df = df.dropna().reset_index(drop=True)
            else:
                df = df.reset_index(drop=True)
            # ---------------------------------------------------------
            # 11. Safety check
            # ---------------------------------------------------------

            if df.empty:
                raise ValueError(
                    "Feature engineering produced an empty dataset."
                )

            logging.info(
                f"Feature engineering completed. "
                f"Shape: {df.shape}"
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

            train_df = self.create_features(train_df)

            test_df = self.create_features(test_df)

            self.save_data(
                train_df,
                test_df
            )

            return train_df, test_df

        except Exception as e:
            raise CustomException(e, sys)