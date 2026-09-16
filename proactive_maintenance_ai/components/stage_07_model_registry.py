import os
import sys
import json
import shutil
from datetime import datetime

from proactive_maintenance_ai.logger.log import logging
from proactive_maintenance_ai.exception.exception_handler import CustomException


class ModelRegistry:

    def __init__(self, config):
        self.config = config

    def get_next_version(self):

        try:
            os.makedirs(
                self.config.registry_dir,
                exist_ok=True
            )

            versions = []

            for item in os.listdir(self.config.registry_dir):

                if item.startswith("v") and os.path.isdir(
                    os.path.join(self.config.registry_dir, item)
                ):

                    try:
                        version = int(item[1:])
                        versions.append(version)

                    except ValueError:
                        continue

            if not versions:
                return 1

            return max(versions) + 1

        except Exception as e:
            raise CustomException(e, sys)

    def register_model(self):

        try:

            logging.info("Starting Model Registration...")

            if not os.path.exists(self.config.model_path):
                raise FileNotFoundError(
                    f"Trained model not found: {self.config.model_path}"
                )

            version = self.get_next_version()

            version_dir = os.path.join(
                self.config.registry_dir,
                f"v{version}"
            )

            os.makedirs(
                version_dir,
                exist_ok=True
            )

            # Copy trained model
            registered_model_path = os.path.join(
                version_dir,
                "model.pkl"
            )

            shutil.copy2(
                self.config.model_path,
                registered_model_path
            )

            # Load evaluation metrics
            metrics = {}

            if os.path.exists(self.config.metrics_path):

                with open(
                    self.config.metrics_path,
                    "r"
                ) as f:

                    metrics = json.load(f)

            # Model metadata
            metadata = {
                "model_version": f"v{version}",
                "registered_at": datetime.now().isoformat(),
                "model_path": registered_model_path,
                "metrics": metrics
            }

            metadata_path = os.path.join(
                version_dir,
                "metadata.json"
            )

            with open(
                metadata_path,
                "w"
            ) as f:

                json.dump(
                    metadata,
                    f,
                    indent=4
                )

            # Update latest model
            latest_model_path = os.path.join(
                self.config.root_dir,
                "latest_model.pkl"
            )

            shutil.copy2(
                registered_model_path,
                latest_model_path
            )

            # Save latest version information
            latest_metadata_path = os.path.join(
                self.config.root_dir,
                "latest_metadata.json"
            )

            latest_metadata = {
                "latest_version": f"v{version}",
                "model_path": latest_model_path,
                "registered_at": metadata["registered_at"],
                "metrics": metrics
            }

            with open(
                latest_metadata_path,
                "w"
            ) as f:

                json.dump(
                    latest_metadata,
                    f,
                    indent=4
                )

            logging.info(
                f"Model registered successfully: v{version}"
            )

            logging.info(
                f"Registered model path: {registered_model_path}"
            )

            logging.info(
                f"Latest model path: {latest_model_path}"
            )

            return version

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_registry(self):

        try:

            logging.info("=" * 60)
            logging.info("MODEL REGISTRY STARTED")
            logging.info("=" * 60)

            version = self.register_model()

            logging.info(
                f"Model Registry Completed. Version: v{version}"
            )

            logging.info("=" * 60)

            return version

        except Exception as e:
            raise CustomException(e, sys)