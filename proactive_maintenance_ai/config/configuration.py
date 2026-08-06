from pathlib import Path

from proactive_maintenance_ai.constant.constants import CONFIG_FILE_PATH
from proactive_maintenance_ai.entity.config_entity import DataIngestionConfig
from proactive_maintenance_ai.utils.common import read_yaml, create_directory


class ConfigurationManager:

    def __init__(
        self,
        config_filepath: Path = CONFIG_FILE_PATH
    ):

        self.config = read_yaml(config_filepath)

        create_directory([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:

        config = self.config.data_ingestion

        create_directory([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=Path(config.root_dir),
            local_data_file=Path(config.local_data_file),
            unzip_dir=Path(config.unzip_dir),
            ingested_data_file=Path(config.ingested_data_file)
        )

        return data_ingestion_config