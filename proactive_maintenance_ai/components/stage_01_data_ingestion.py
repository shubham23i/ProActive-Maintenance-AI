import os
import sys
import shutil
import zipfile

from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.exception.exception_handler import CustomException


class DataIngestion:
    def __init__(self, config):
        self.config = config

    def extract_data(self):
        """
        Extract the zip file into the ingestion directory.
        """

        try:
            zip_path = self.config.local_data_file
            unzip_path = self.config.unzip_dir

            if not os.path.exists(zip_path):
                raise FileNotFoundError(f"Dataset not found: {zip_path}")

            os.makedirs(unzip_path, exist_ok=True)

            logging.info(f"Extracting dataset from {zip_path}")

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(unzip_path)

            logging.info(f"Dataset extracted successfully to {unzip_path}")

        except Exception as e:
            raise CustomException(e, sys)

    def rename_csv(self):
        """
        Locate the extracted CSV and rename it to raw_data.csv.
        """

        try:
            extracted_csv = None

            for root, _, files in os.walk(self.config.unzip_dir):
                for file in files:
                    if file.endswith(".csv"):
                        extracted_csv = os.path.join(root, file)
                        break

                if extracted_csv:
                    break

            if extracted_csv is None:
                raise FileNotFoundError("No CSV file found after extraction.")

            destination = self.config.ingested_data_file

            if os.path.exists(destination):
                os.remove(destination)

            shutil.move(extracted_csv, destination)

            logging.info(f"CSV saved at {destination}")

            return destination

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self):
        """
        Execute the complete data ingestion pipeline.
        """

        try:
            logging.info("=" * 60)
            logging.info("Data Ingestion Started")
            logging.info("=" * 60)

            self.extract_data()

            ingested_data_path = self.rename_csv()

            logging.info("=" * 60)
            logging.info("Data Ingestion Completed")
            logging.info("=" * 60)

            return ingested_data_path

        except Exception as e:
            raise CustomException(e, sys)