import os
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

            logging.info("reading df")
            df = pd.read_csv(self.config.data_file)
            schema = self.read_schema()
            expected_columns = schema["columns"]
            validation_status=True
            missing_columns = []
            datatype_mismatch = []

            for column in expected_columns.keys():
                if column not in df.columns:
                    missing_columns.append(column)
                    validation_status = False

            for column, expected_dtype in expected_columns.items():

                if column not in df.columns:
                    continue

                series = df[column]

                if expected_dtype == "int64":
                    valid = is_integer_dtype(series)

                elif expected_dtype == "float64":
                    valid = is_float_dtype(series)

                elif expected_dtype == "object":
                    valid = is_object_dtype(series) or is_string_dtype(series)

                else:
                    valid = True

                if not valid:
                    datatype_mismatches.append(
                        f"{column}: expected {expected_dtype}, got {series.dtype}"
                    )
                    validation_status = False
            target_column = schema["target_column"]
            if target_column not in df.columns:
                validation_status = False

            with open(self.config.status_file, "w") as f:

                f.write(f"Validation Status: {validation_status}\n\n")

                f.write("Missing Columns:\n")

                if missing_columns:
                    for col in missing_columns:
                        f.write(f"{col}\n")
                else:
                    f.write("None\n")

                f.write("\nDatatype Mismatches:\n")

                if datatype_mismatch:
                    for mismatch in datatype_mismatch:
                        f.write(f"{mismatch}\n")
                else:
                    f.write("None\n")

                f.write(f"\nTarget Column: {target_column}")

            logging.info("Data Validation Completed.")

            return validation_status

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_validation(self):
        try:
            logging.info("=" * 60)
            logging.info("Data Validation Started")
            logging.info("=" * 60)

            validation_status = self.validate_dataset()
            logging.info(f"Validation Status: {validation_status}")
            logging.info("=" * 60)
            logging.info("Data Validation Completed")
            logging.info("=" * 60)

            return validation_status
        except Exception as e:
            raise CustomException(e, sys)






