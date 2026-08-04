from proactive_maintenance_ai.exception.exception_handler import CustomException
import sys

try:
    a=1/0
except Exception as e:
    raise CustomException(e,sys)