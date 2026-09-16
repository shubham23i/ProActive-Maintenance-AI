
import sys
import pandas as pd
import sys
from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.exception.exception_handler import CustomException


class DataPreprocessing:

    def __init__(self, config):

        self.config = config

        # Used only for chronological ordering
        self.order_column = "UDI"

        self.feature_columns = [
            "Type",
            "Air temperature [K]",
            "Process temperature [K]",
            "Rotational speed [rpm]",
            "Torque [Nm]",
            "Tool wear [min]"
        ]

        self.target_column = "Machine failure"

    def load_data(self):

        try:

            df = pd.read_csv(
                self.config.input_data_file
            )

            logging.info(
                f"Raw dataset loaded: {df.shape}"
            )

            return df

        except Exception as e:
            raise CustomException(e, sys)

    def preprocess_data(self, df):

        try:

            # ---------------------------------------------------------
            # Keep required columns
            # ---------------------------------------------------------

            columns_to_keep = [
                self.order_column,
                *self.feature_columns,
                self.target_column
            ]

            df = df[columns_to_keep].copy()

            # ---------------------------------------------------------
            # Sort chronologically
            # ---------------------------------------------------------

            df = (
                df.sort_values(
                    by=self.order_column
                )
                .reset_index(drop=True)
            )

            logging.info(
                f"Data sorted using {self.order_column}"
            )

            # ---------------------------------------------------------
            # Remove missing values
            # ---------------------------------------------------------

            initial_rows = len(df)

            df = (
                df.dropna()
                .reset_index(drop=True)
            )

            removed_rows = initial_rows - len(df)

            logging.info(
                f"Removed {removed_rows} rows containing missing values"
            )

            # ---------------------------------------------------------
            # Chronological train/test split
            # ---------------------------------------------------------

            split_index = int(
                len(df) * 0.85
            )

            train_df = df.iloc[
                :split_index
            ].copy()

            test_df = df.iloc[
                split_index:
            ].copy()

            # ---------------------------------------------------------
            # Log split information
            # ---------------------------------------------------------

            logging.info(
                f"Training data shape: "
                f"{train_df.shape}"
            )

            logging.info(
                f"Testing data shape: "
                f"{test_df.shape}"
            )

            logging.info(
                f"Train UDI range: "
                f"{train_df[self.order_column].min()} - "
                f"{train_df[self.order_column].max()}"
            )

            logging.info(
                f"Test UDI range: "
                f"{test_df[self.order_column].min()} - "
                f"{test_df[self.order_column].max()}"
            )

            # ---------------------------------------------------------
            # Target distribution
            # ---------------------------------------------------------

            logging.info(
                f"Train target distribution:\n"
                f"{train_df[self.target_column].value_counts().to_dict()}"
            )

            logging.info(
                f"Test target distribution:\n"
                f"{test_df[self.target_column].value_counts().to_dict()}"
            )

            return train_df, test_df

        except Exception as e:

            raise CustomException(e, sys)

    def save_data(
        self,
        train_df,
        test_df
    ):

        try:

            train_df.to_csv(
                self.config.train_data_file,
                index=False
            )

            test_df.to_csv(
                self.config.test_data_file,
                index=False
            )

            logging.info(
                "Preprocessed train and test datasets saved successfully."
            )

        except Exception as e:

            raise CustomException(e, sys)

    def initiate_data_preprocessing(self):

        try:

            logging.info("=" * 60)
            logging.info(
                "Data Preprocessing Started"
            )
            logging.info("=" * 60)

            df = self.load_data()

            train_df, test_df = (
                self.preprocess_data(df)
            )

            self.save_data(
                train_df,
                test_df
            )

            logging.info(
                "Data Preprocessing Completed"
            )

            return train_df, test_df

        except Exception as e:

            raise CustomException(e, sys)

