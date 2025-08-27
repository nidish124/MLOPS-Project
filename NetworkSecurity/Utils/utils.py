import os
import sys
import yaml
import numpy as np
from NetworkSecurity.Logging.logger import logging
from NetworkSecurity.Execption.execption import Custom_execption
import dill
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

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
    
def numpy_array_load(arr: np.array,file_path:str):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path,'wb') as file:
            np.save(file,arr)
    except Exception as e:
        raise Custom_execption(e,sys)
    
def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise Custom_execption(e, sys)

def load_object(file_path:str):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        else:
            raise Exception(f"file :{file_path} not exist")
    except Exception as e:
        raise Custom_execption(e,sys)
    
def load_numpy_array_data(file_path:str):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                return np.load(file)
        else:
            raise Exception(f"file :{file_path} not exist")
    except Exception as e:
        raise Custom_execption(e,sys)
    
def evaluate_models(x_train, y_train, x_test, y_test, models, parms):
    try:
        report = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            parm = parms[list(models.keys())[i]]

            gcv = GridSearchCV(model, parm, cv = 3)
            gcv.fit(x_train, y_train)

            model.set_params(**gcv.best_params_)
            model.fit(x_train,y_train)

            y_train_pred = model.predict(x_train)

            y_test_pred = model.predict(x_test)

            train_model_score = r2_score(y_true= y_train, y_pred=y_train_pred)
            test_model_score = r2_score(y_true= y_test, y_pred=y_test_pred)

            report[list(models.keys())[i]] = test_model_score
            
        return report
    except Exception as e:
        raise Custom_execption(e,sys)
    