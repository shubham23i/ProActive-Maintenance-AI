import os
from box.exceptions import BoxValueError
import yaml
from proactive_maintenance_ai.logger.log import logging
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64
from pathlib import Path

CONFIG_FILE_PATH = Path("config/config.yaml")
PARAMS_FILE_PATH = Path("params.yaml")

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    try:
        with open(path_to_yaml) as yaml_file:
            content=yaml.safe_load(yaml_file)
            logging.info(f"file {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError as e:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e

@ensure_annotations
def create_directory(path_to_dir:list, verbose=True):
    for path in path_to_dir:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logging.info(f"created directory at {path}")

@ensure_annotations
def save_json(path:Path, data:dict):
    with open(path, 'w') as f:
        json.dump(data, f,indent=4)
    logging.info(f"saved json file at {path}")

@ensure_annotations
def load_json(path:Path)->ConfigBox:
    with open(path) as f:
        content=json.load(f)
    logging.info(f"json file loaded successfully from {path}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(data:any, path:Path):
    joblib.dump(value=data, filename=path)
    logging.info(f"saved binary file at {path}")

@ensure_annotations
def load_bin(path:Path)->Any:
    data=joblib.load(path)
    logging.info(f"binary file loaded successfully from {path}")
    return data

@ensure_annotations
def get_size(path:Path)->str:
    size_in_kb=round(os.path.getsize(path)/1024)

    return f"{size_in_kb} KB"

def decode_image(ingstring, filename):
    imgdata = base64.b64decode(ingstring)
    with open(filename, 'wb') as f:
        f.write(imgdata)
        f.close()

def encode_image_into_base64(filename):
    with open(filename, 'rb') as f: 
        return base64.b64encode(f.read())