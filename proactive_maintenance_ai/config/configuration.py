from pathlib import Path

from proactive_maintenance_ai.constant.constants import CONFIG_FILE_PATH
from proactive_maintenance_ai.entity.config_entity import DataIngestionConfig,DataValidationConfig, DataPreprocessingConfig,FeatureEngineeringConfig,ModelTrainerConfig,ModelEvaluationConfig,ModelRegistryConfig,PredictionConfig
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
    

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        create_directory([config.root_dir])
        return DataValidationConfig(            
            root_dir=Path(config.root_dir),
            status_file=Path(config.status_file),
            schema_file=Path(config.schema_file),
            data_file=Path(config.data_file)
        )

    def get_data_preprocessing_config(self) -> DataPreprocessingConfig:

        config = self.config.data_preprocessing

        create_directory([config.root_dir])

        return DataPreprocessingConfig(
            root_dir=Path(config.root_dir),
            input_data_file=Path(config.input_data_file),
            train_data_file=Path(config.train_data_file),
            test_data_file=Path(config.test_data_file),
            preprocessor_file=Path(config.preprocessor_file)
        )

    def get_feature_engineering_config(self) -> FeatureEngineeringConfig:

        config = self.config.feature_engineering

        create_directory([config.root_dir])

        return FeatureEngineeringConfig(
            root_dir=Path(config.root_dir),

            input_train_data_file=Path(
                config.input_train_data_file
            ),

            input_test_data_file=Path(
                config.input_test_data_file
            ),

            output_train_data_file=Path(
                config.output_train_data_file
            ),

            output_test_data_file=Path(
                config.output_test_data_file
            )
        )
    def get_model_trainer_config(self) -> ModelTrainerConfig:

        config = self.config.model_training
        create_directory([config.root_dir])
        return ModelTrainerConfig(
            root_dir=Path(config.root_dir),
            input_train_data_file=Path(config.input_train_data_file),
            input_test_data_file=Path(config.input_test_data_file),
            trained_model_path=Path(config.trained_model_path),
            target_column=config.target_column
        )

    def get_model_evaluation_config(
        self
    ) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
        create_directory([
            config.root_dir
        ])
        return ModelEvaluationConfig(
            root_dir=Path(
                config.root_dir
            ),
            model_path=Path(
                config.model_path
            ),
            test_data_path=Path(
                config.test_data_path
            ),
            target_column=config.target_column,
            metrics_file=Path(
                config.metrics_file
            ),
            confusion_matrix_path=Path(
                config.confusion_matrix_path
            )
        )

    def get_model_registry_config(
        self
    ) -> ModelRegistryConfig:

        config = self.config.model_registry

        create_directory([
            config.root_dir,
            config.registry_dir
        ])

        return ModelRegistryConfig(

            root_dir=Path(
                config.root_dir
            ),

            registry_dir=Path(
                config.registry_dir
            ),

            model_path=Path(
                config.model_path
            ),

            metrics_path=Path(
                config.metrics_path
            )
        )

    def get_prediction_config(self) -> PredictionConfig:

        config = self.config.prediction

        create_directory([
            config.root_dir
        ])

        return PredictionConfig(

            root_dir=Path(
                config.root_dir
            ),

            model_path=Path(
                config.model_path
            )
        )