from proactive_maintenance_ai.config.configuration import ConfigurationManager
from proactive_maintenance_ai.components.stage_01_data_ingestion import DataIngestion

from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.exception.exception_handler import CustomException


class TrainingPipeline:

    def __init__(self):
        pass

    def start_data_ingestion(self):

        config = ConfigurationManager()

        data_ingestion_config = config.get_data_ingestion_config()

        data_ingestion = DataIngestion(data_ingestion_config)

        data_ingestion.initiate_data_ingestion()

    def run_pipeline(self):

        logging.info("=" * 50)
        logging.info("Training Pipeline Started")
        logging.info("=" * 50)

        self.start_data_ingestion()

        logging.info("=" * 50)
        logging.info("Training Pipeline Completed")
        logging.info("=" * 50)