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
    input_train_data_file: Path
    input_test_data_file: Path
    trained_model_path: Path
    target_column: str


@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    model_path: Path
    test_data_path: Path
    target_column: str
    metrics_file: Path
    confusion_matrix_path: Path


@dataclass(frozen=True)
class ModelRegistryConfig:
    root_dir: Path
    registry_dir: Path
    model_path: Path
    metrics_path: Path

@dataclass(frozen=True)
class PredictionConfig:
    root_dir: Path
    model_path: Path
    raw_data_file: Path


@dataclass(frozen=True)
class AnomalyDetectionConfig:
    root_dir: Path
    data_file: Path
    model_path: Path


@dataclass(frozen=True)
class ModelExplainabilityConfig:
    root_dir: Path
    model_path: Path