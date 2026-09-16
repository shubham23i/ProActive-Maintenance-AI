import sys

from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.exception.exception_handler import CustomException


class MaintenanceDecisionEngine:

    def __init__(self):
        pass

    def generate_decision(
        self,
        risk_level,
        anomaly_status
    ):

        try:

            if risk_level == "HIGH" and anomaly_status == "ANOMALY":

                maintenance_priority = "CRITICAL"

                recommended_action = (
                    "Immediately stop or isolate the machine and "
                    "perform an urgent inspection. Investigate "
                    "potential component failure."
                )

                inspection_window = "Immediately"

            elif risk_level == "HIGH":

                maintenance_priority = "URGENT"

                recommended_action = (
                    "Inspect machine immediately and consider "
                    "planned shutdown or component replacement."
                )

                inspection_window = "Within 24 hours"

            elif (
                risk_level == "MEDIUM"
                and anomaly_status == "ANOMALY"
            ):

                maintenance_priority = "HIGH"

                recommended_action = (
                    "Investigate abnormal sensor behavior and "
                    "schedule preventive maintenance."
                )

                inspection_window = "Within 48 hours"

            elif risk_level == "MEDIUM":

                maintenance_priority = "HIGH"

                recommended_action = (
                    "Schedule preventive inspection and monitor "
                    "sensor trends closely."
                )

                inspection_window = "Within 7 days"

            elif anomaly_status == "ANOMALY":

                maintenance_priority = "MEDIUM"

                recommended_action = (
                    "Investigate abnormal sensor behavior and "
                    "continue enhanced monitoring."
                )

                inspection_window = "Within 7 days"

            else:

                maintenance_priority = "ROUTINE"

                recommended_action = (
                    "Continue normal operation and monitor "
                    "sensor trends."
                )

                inspection_window = "30+ days"

            result = {
                "maintenance_priority": maintenance_priority,
                "recommended_action": recommended_action,
                "inspection_window": inspection_window
            }

            logging.info(
                f"Maintenance decision: {result}"
            )

            return result

        except Exception as e:
            raise CustomException(e, sys)