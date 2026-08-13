import os
import sys
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.exception.exception_handler import CustomException


class DataPreprocessing:

    def __init__(self, config):
        self.config = config

        self.target_column = "Machine failure"

        self.feature_columns = [
            "Type",
            "Air temperature [K]",
            "Process temperature [K]",
            "Rotational speed [rpm]",
            "Torque [Nm]",
            "Tool wear [min]"
        ]

        self.categorical_columns = [
            "Type"
        ]

        self.numerical_columns = [
            "Air temperature [K]",
            "Process temperature [K]",
            "Rotational speed [rpm]",
            "Torque [Nm]",
            "Tool wear [min]"
        ]

    def load_data(self):
        """
        Load the ingested dataset.
        """

        try:

            logging.info(
                f"Loading data from {self.config.input_data_file}"
            )

            df = pd.read_csv(self.config.input_data_file)

            logging.info(
                f"Dataset loaded successfully. Shape: {df.shape}"
            )

            return df

        except Exception as e:
            raise CustomException(e, sys)

    def clean_data(self, df):
        """
        Remove unnecessary columns, duplicates
        and handle missing values.
        """

        try:

            logging.info("Starting data cleaning...")

            # Keep only required columns
            columns_to_keep = self.feature_columns + [
                self.target_column
            ]

            df = df[columns_to_keep].copy()

            # Remove duplicate rows
            duplicate_count = df.duplicated().sum()

            if duplicate_count > 0:

                logging.info(
                    f"Removing {duplicate_count} duplicate rows"
                )

                df = df.drop_duplicates()

            # Check missing values
            missing_values = df.isnull().sum().sum()

            if missing_values > 0:

                logging.info(
                    f"Found {missing_values} missing values"
                )

                # Numerical columns
                for column in self.numerical_columns:
                    if df[column].isnull().any():
                        df[column] = df[column].fillna(
                            df[column].median()
                        )

                # Categorical columns
                for column in self.categorical_columns:
                    if df[column].isnull().any():
                        df[column] = df[column].fillna(
                            df[column].mode()[0]
                        )

                # Target column
                if df[self.target_column].isnull().any():
                    df = df.dropna(
                        subset=[self.target_column]
                    )

            logging.info(
                f"Data cleaning completed. Shape: {df.shape}"
            )

            return df

        except Exception as e:
            raise CustomException(e, sys)

    def split_data(self, df):
        """
        Split the dataset into training and testing sets.
        """

        try:

            logging.info("Splitting data into train and test sets...")

            X = df[self.feature_columns]
            y = df[self.target_column]

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42,
                stratify=y
            )

            train_df = X_train.copy()
            train_df[self.target_column] = y_train

            test_df = X_test.copy()
            test_df[self.target_column] = y_test

            logging.info(
                f"Training data shape: {train_df.shape}"
            )

            logging.info(
                f"Testing data shape: {test_df.shape}"
            )

            return train_df, test_df

        except Exception as e:
            raise CustomException(e, sys)

    def create_preprocessor(self):
        """
        Create preprocessing pipeline for categorical
        and numerical features.
        """

        try:

            logging.info("Creating preprocessing pipeline...")

            preprocessor = ColumnTransformer(
                transformers=[
                    (
                        "categorical",
                        OneHotEncoder(
                            handle_unknown="ignore",
                            sparse_output=False
                        ),
                        self.categorical_columns
                    )
                ],
                remainder="passthrough"
            )

            logging.info(
                "Preprocessing pipeline created successfully."
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def save_data(self, train_df, test_df):

        try:

            # Create output directory only
            os.makedirs(
                self.config.root_dir,
                exist_ok=True
            )

            # Save train data
            train_df.to_csv(
                self.config.train_data_file,
                index=False
            )

            # Save test data
            test_df.to_csv(
                self.config.test_data_file,
                index=False
            )

            logging.info(
                f"Training data saved to: {self.config.train_data_file}"
            )

            logging.info(
                f"Testing data saved to: {self.config.test_data_file}"
            )

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_preprocessing(self):

        try:

            logging.info("=" * 60)
            logging.info("Data Preprocessing Started")
            logging.info("=" * 60)

            # Load data
            df = self.load_data()

            # Clean data
            df = self.clean_data(df)

            # Split data
            train_df, test_df = self.split_data(df)

            # Create preprocessing pipeline
            preprocessor = self.create_preprocessor()

            # Fit ONLY on training data
            preprocessor.fit(
                train_df[self.feature_columns]
            )

            # Save preprocessor
            joblib.dump(
                preprocessor,
                self.config.preprocessor_file
            )

            logging.info(
                f"Preprocessor saved to "
                f"{self.config.preprocessor_file}"
            )

            # Save train/test datasets
            self.save_data(
                train_df,
                test_df
            )

            logging.info("=" * 60)
            logging.info(
                "Data Preprocessing Completed Successfully"
            )
            logging.info("=" * 60)

            return (
                self.config.train_data_file,
                self.config.test_data_file,
                self.config.preprocessor_file
            )

        except Exception as e:
            raise CustomException(e, sys)