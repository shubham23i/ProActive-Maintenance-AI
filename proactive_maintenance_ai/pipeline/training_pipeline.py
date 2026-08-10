import sys

from proactive_maintenance_ai.config.configuration import ConfigurationManager
from proactive_maintenance_ai.components.stage_01_data_ingestion import DataIngestion
from proactive_maintenance_ai.components.stage_02_data_validation import DataValidation
from proactive_maintenance_ai.components.stage_03_data_preprocessing import DataPreprocessing

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


    def start_data_preprocessing(self):

        logging.info("Starting Data Preprocessing...")
        data_preprocessing_config = (
            self.config.get_data_preprocessing_config()
            )
        data_preprocessing = DataPreprocessing(
            data_preprocessing_config
        )
        train_data_path, test_data_path, preprocessor_path = (
            data_preprocessing.initiate_data_preprocessing()
        )
        logging.info("Data Preprocessing Completed.")

        return (
            train_data_path,
            test_data_path,
            preprocessor_path
        )
    def run_pipeline(self):

        try:

            logging.info("=" * 60)
            logging.info("Training Pipeline Started")
            logging.info("=" * 60)

            self.start_data_ingestion()

            self.start_data_validation()
            self.start_data_preprocessing()

            logging.info("=" * 60)
            logging.info("Training Pipeline Completed Successfully")
            logging.info("=" * 60)

        except Exception as e:
            raise CustomException(e, sys)