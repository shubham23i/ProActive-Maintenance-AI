import sys
import pandas as pd
from pandas.api.types import (
    is_integer_dtype,
    is_float_dtype,
    is_object_dtype,
    is_string_dtype
)
import yaml

from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.exception.exception_handler import CustomException


class DataValidation:

    def __init__(self, config):
        self.config = config

    def read_schema(self):

        try:

            with open(self.config.schema_file, "r") as f:
                schema = yaml.safe_load(f)

            return schema

        except Exception as e:
            raise CustomException(e, sys)

    def validate_dataset(self):

        try:

            logging.info("Reading dataset")

            df = pd.read_csv(
                self.config.data_file
            )

            schema = self.read_schema()

            expected_columns = schema["columns"]

            validation_status = True

            missing_columns = []
            datatype_mismatches = []

            # ---------------------------------------------------------
            # Check missing columns
            # ---------------------------------------------------------

            for column in expected_columns.keys():

                if column not in df.columns:

                    missing_columns.append(column)

                    validation_status = False

            # ---------------------------------------------------------
            # Check data types
            # ---------------------------------------------------------

            for column, expected_dtype in expected_columns.items():

                if column not in df.columns:
                    continue

                series = df[column]

                actual_dtype = str(series.dtype)

                # Integer
                if expected_dtype == "int64":

                    valid = is_integer_dtype(series)

                # Float
                elif expected_dtype == "float64":

                    valid = is_float_dtype(series)

                # Object / String
                elif expected_dtype == "object":

                    valid = (
                        is_object_dtype(series)
                        or is_string_dtype(series)
                    )

                else:

                    valid = True

                # -----------------------------------------------------
                # Record mismatch
                # -----------------------------------------------------

                if not valid:

                    datatype_mismatches.append(
                        f"{column}: expected {expected_dtype}, "
                        f"got {actual_dtype}"
                    )

                    validation_status = False

            # ---------------------------------------------------------
            # Check target column
            # ---------------------------------------------------------

            target_column = schema["target_column"]

            if target_column not in df.columns:

                validation_status = False

            # ---------------------------------------------------------
            # Write validation report
            # ---------------------------------------------------------

            with open(
                self.config.status_file,
                "w"
            ) as f:

                f.write(
                    f"Validation Status: "
                    f"{validation_status}\n\n"
                )

                # Missing columns
                f.write(
                    "Missing Columns:\n"
                )

                if missing_columns:

                    for col in missing_columns:
                        f.write(f"{col}\n")

                else:

                    f.write("None\n")

                # Datatype mismatches
                f.write(
                    "\nDatatype Mismatches:\n"
                )

                if datatype_mismatches:

                    for mismatch in datatype_mismatches:
                        f.write(f"{mismatch}\n")

                else:

                    f.write("None\n")

                # Target column
                f.write(
                    f"\nTarget Column: "
                    f"{target_column}\n"
                )

                if target_column in df.columns:

                    f.write(
                        "Target Column Status: Present\n"
                    )

                else:

                    f.write(
                        "Target Column Status: Missing\n"
                    )

            logging.info(
                "Data Validation Completed."
            )

            return validation_status

        except Exception as e:

            raise CustomException(e, sys)

    def initiate_data_validation(self):

        try:

            logging.info("=" * 60)
            logging.info("Data Validation Started")
            logging.info("=" * 60)

            validation_status = (
                self.validate_dataset()
            )

            logging.info(
                f"Validation Status: "
                f"{validation_status}"
            )

            logging.info("=" * 60)
            logging.info(
                "Data Validation Completed"
            )
            logging.info("=" * 60)

            return validation_status

        except Exception as e:

            raise CustomException(e, sys)
