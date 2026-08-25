import sys
import logging

from proactive_maintenance_ai.config.configuration import ConfigurationManager

from proactive_maintenance_ai.components.stage_01_data_ingestion import DataIngestion
from proactive_maintenance_ai.components.stage_02_data_validation import DataValidation
from proactive_maintenance_ai.components.stage_03_data_preprocessing import DataPreprocessing
from proactive_maintenance_ai.components.stage_04_feature_engineering import FeatureEngineering
from proactive_maintenance_ai.components.stage_05_model_trainer import ModelTrainer
from proactive_maintenance_ai.components.stage_06_model_evaluation import ModelEvaluation
from proactive_maintenance_ai.components.stage_07_model_registry import (
    ModelRegistry
)

from proactive_maintenance_ai.exception.exception_handler import CustomException


class TrainingPipeline:

    def __init__(self):
        self.config = ConfigurationManager()

    def start_data_ingestion(self):

        try:

            logging.info("Starting Data Ingestion...")

            config = self.config.get_data_ingestion_config()

            data_ingestion = DataIngestion(config)

            data_ingestion.initiate_data_ingestion()

            logging.info("Data Ingestion Completed.")

        except Exception as e:
            raise CustomException(e, sys)

    def start_data_validation(self):

        try:

            logging.info("Starting Data Validation...")

            config = self.config.get_data_validation_config()

            data_validation = DataValidation(config)

            validation_status = (
                data_validation.initiate_data_validation()
            )

            if not validation_status:
                raise Exception("Data Validation Failed")

            logging.info("Data Validation Completed.")

        except Exception as e:
            raise CustomException(e, sys)

    def start_data_preprocessing(self):

        try:

            logging.info("Starting Data Preprocessing...")

            config = (
                self.config.get_data_preprocessing_config()
            )

            data_preprocessing = DataPreprocessing(
                config
            )

            data_preprocessing.initiate_data_preprocessing()

            logging.info(
                "Data Preprocessing Completed."
            )

        except Exception as e:
            raise CustomException(e, sys)

    def start_feature_engineering(self):

        try:

            logging.info("Starting Feature Engineering...")

            config = (
                self.config.get_feature_engineering_config()
            )

            feature_engineering = FeatureEngineering(
                config
            )

            feature_engineering.initiate_feature_engineering()

            logging.info(
                "Feature Engineering Completed."
            )

        except Exception as e:
            raise CustomException(e, sys)

    def start_model_training(self):

        try:

            logging.info("Starting Model Training...")

            config = (
                self.config.get_model_trainer_config()
            )

            model_trainer = ModelTrainer(
                config
            )

            model_trainer.initiate_model_training()

            logging.info(
                "Model Training Completed."
            )

        except Exception as e:
            raise CustomException(e, sys)

    def start_model_evaluation(self):

        try:

            logging.info("Starting Model Evaluation...")

            config = (
                self.config.get_model_evaluation_config()
            )

            model_evaluation = ModelEvaluation(
                config
            )

            metrics = (
                model_evaluation.initiate_model_evaluation()
            )

            logging.info(
                "Model Evaluation Completed."
            )

            return metrics

        except Exception as e:
            raise CustomException(e, sys)

    def start_model_registry(self):

        try:

            logging.info(
                "Starting Model Registry..."
            )

            config = (
                self.config.get_model_registry_config()
            )

            model_registry = ModelRegistry(
                config
            )

            version = (
                model_registry.initiate_model_registry()
            )

            logging.info(
                f"Model Registry Completed. "
                f"Version: v{version}"
            )

            return version

        except Exception as e:
            raise CustomException(e, sys)

    def run_pipeline(self):

        try:

            logging.info("=" * 60)
            logging.info("TRAINING PIPELINE STARTED")
            logging.info("=" * 60)

            self.start_data_ingestion()

            self.start_data_validation()

            self.start_data_preprocessing()

            self.start_feature_engineering()

            self.start_model_training()

            self.start_model_evaluation()

            self.start_model_registry()

            logging.info("=" * 60)
            logging.info("TRAINING PIPELINE COMPLETED")
            logging.info("=" * 60)

        except Exception as e:
            raise CustomException(e, sys)