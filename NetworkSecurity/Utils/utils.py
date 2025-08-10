import os
import sys
import yaml
from NetworkSecurity.Logging.logger import logging
from NetworkSecurity.Execption.execption import Custom_execption

def read_yaml(file_path) -> dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise Custom_execption(e,sys)

def write_yaml(file_path:str, content, replace: bool) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as file:
            yaml.dump(content, file)
    except Exception as e:
        raise Custom_execption(e,sys)