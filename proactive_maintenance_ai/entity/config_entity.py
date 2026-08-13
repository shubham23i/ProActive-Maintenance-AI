from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    local_data_file: Path
    unzip_dir: Path
    ingested_data_file: Path


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    status_file: Path
    schema_file: Path
    data_file: Path


@dataclass(frozen=True)
class DataPreprocessingConfig:
    root_dir: Path
    input_data_file: Path
    train_data_file: Path
    test_data_file: Path
    preprocessor_file: Path


@dataclass(frozen=True)
class FeatureEngineeringConfig:
    root_dir: Path
    input_train_data_file: Path
    input_test_data_file: Path
    output_train_data_file: Path    
    output_test_data_file: Path


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    trained_model_path: Path


@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    metrics_file_path: Path