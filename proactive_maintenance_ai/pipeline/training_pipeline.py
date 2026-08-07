import sys

from proactive_maintenance_ai.config.configuration import ConfigurationManager
from proactive_maintenance_ai.components.stage_01_data_ingestion import DataIngestion
from proactive_maintenance_ai.components.stage_02_data_validation import DataValidation

from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.exception.exception_handler import CustomException


class TrainingPipeline:

    def __init__(self):
        self.config = ConfigurationManager()

    def start_data_ingestion(self):

        logging.info("Starting Data Ingestion...")

        data_ingestion_config = self.config.get_data_ingestion_config()

        data_ingestion = DataIngestion(data_ingestion_config)

        data_ingestion.initiate_data_ingestion()

        logging.info("Data Ingestion Completed.")

    def start_data_validation(self):

        logging.info("Starting Data Validation...")

        data_validation_config = self.config.get_data_validation_config()

        data_validation = DataValidation(data_validation_config)

        validation_status = data_validation.initiate_data_validation()

        if not validation_status:
            raise ValueError("Data Validation Failed")

        logging.info("Data Validation Completed.")

    def run_pipeline(self):

        try:

            logging.info("=" * 60)
            logging.info("Training Pipeline Started")
            logging.info("=" * 60)

            self.start_data_ingestion()

            self.start_data_validation()

            logging.info("=" * 60)
            logging.info("Training Pipeline Completed Successfully")
            logging.info("=" * 60)

        except Exception as e:
            raise CustomException(e, sys)