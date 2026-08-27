import sys

from proactive_maintenance_ai.config.configuration import ConfigurationManager
from proactive_maintenance_ai.components.stage_08_prediction import Prediction
from proactive_maintenance_ai.exception.exception_handler import CustomException


class PredictionPipeline:

    def __init__(self):
        self.config = ConfigurationManager()

    def start_prediction(self, input_data):

        try:
            prediction_config = self.config.get_prediction_config()

            prediction = Prediction(prediction_config)

            result = prediction.initiate_prediction(input_data)

            return result

        except Exception as e:
            raise CustomException(e, sys)