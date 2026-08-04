import sys
import os
from pathlib import Path
import logging


project_name = "proactive_maintenance_ai"

list_of_files = [

    # Components
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/stage_01_data_ingestion.py",
    f"{project_name}/components/stage_02_data_validation.py",
    f"{project_name}/components/stage_03_data_preprocessing.py",
    f"{project_name}/components/stage_04_feature_engineering.py",
    f"{project_name}/components/stage_05_model_trainer.py",
    f"{project_name}/components/stage_06_model_evaluation.py",
    f"{project_name}/components/stage_07_model_registry.py",
    f"{project_name}/components/stage_08_prediction.py",

    # Configuration
    f"{project_name}/config/__init__.py",
    f"{project_name}/config/configuration.py",

    # Constants
    f"{project_name}/constant/__init__.py",
    f"{project_name}/constant/constants.py",

    # Entity
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/entity/artifact_entity.py",

    # Pipeline
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/training_pipeline.py",
    f"{project_name}/pipeline/prediction_pipeline.py",

    # Utilities
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/common.py",
    f"{project_name}/utils/model_utils.py",

    # Logger
    f"{project_name}/logger/__init__.py",
    f"{project_name}/logger/log.py",

    # Exception
    f"{project_name}/exception/__init__.py",
    f"{project_name}/exception/exception_handler.py",

    # Configuration files
    "config/config.yaml",
    "config/params.yaml",
    "config/schema.yaml",

    # MLflow
    "mlruns/.gitkeep",

    # Data
    "data/raw/.gitkeep",
    "data/processed/.gitkeep",

    # Artifacts
    "artifacts/.gitkeep",

    # Models
    "models/.gitkeep",

    # Reports
    "reports/.gitkeep",

    # Notebooks
    "notebooks/EDA.ipynb",
    "notebooks/Model_Training.ipynb",

    # Tests
    "tests/__init__.py",
    "tests/test_data_validation.py",
    "tests/test_model.py",

    # API
    "app.py",
    "api.py",

    # Streamlit
    "streamlit_app.py",

    # Deployment
    "Dockerfile",
    ".dockerignore",
    "docker-compose.yml",

    # CI/CD
    ".github/workflows/main.yaml",

    # Project files
    "requirements.txt",
    "setup.py",
    "README.md",
    ".gitignore"

]


for file_path in list_of_files:
    file_path = Path(file_path)
    filedir,filename = os.path.split(file_path)

    if filedir!="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Directory {filedir} created")
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path)==0):        
        with open(file_path, "w") as f:
            pass
        logging.info(f"File {filename} created")
    else:
        logging.info(f"File {filename} already exists")
    

