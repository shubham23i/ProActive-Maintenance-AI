import sys

from proactive_maintenance_ai.pipeline.training_pipeline import TrainingPipeline

from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.exception.exception_handler import CustomException


if __name__ == "__main__":

    try:

        logging.info("Application Started")

        pipeline = TrainingPipeline()

        pipeline.run_pipeline()

        logging.info("Application Finished Successfully")

    except Exception as e:
        logging.exception(e)
        raise CustomException(e, sys)