import os
import sys
import numpy as np
import pandas as pd

"""
defining common constant variable for training pipeline
"""
TARGET_COLUMN = 'Result'
PIPELINE_NAME: str = 'NetworkSecurity'
ARTIFACT_DIR: str = 'Artifact'
FILE_NAME: str = 'phisingData.csv'
TRAIN_FILE_NAME: str = 'train.csv'
TEST_FILE_NAME: str = 'test.csv'
SCHEMA_FILE_NAME: str = os.path.join("data_schema", 'schema.yaml')
MODEL_FILE_NAME :str = os.path.join("Model", 'model.pkl')


""" Environment variable for MongoDB connection """
COLLECTION_NAME: str = 'Network_Data'
DATABASE_NAME: str = 'NetworkSecurity'
DATA_INGESTION_DIRNAME: str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR: str = "Feature_Store"
DATA_INGESTION_INGESTION_DIR: str = "Ingestion"
TRAIN_TEST_SPLIT_RATIO: float = 0.2

""" Data Validation related constant start with Data_validation var name"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"

""" Data Transformation related constant start with Data_transformation var name"""

DATA_TRANSFORMATION_DIR = 'data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = 'transformed'
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR = 'transformed_obj'
DATA_TRANSFORMATION_TRAIN_FILE = 'train.npy'
DATA_TRANSFORMATION_TEST_FILE = 'test.npy'
DATA_TRANSFORMATION_INPUT_PARMS = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}

""" Model trainer constant variables"""
MODEL_TRAINER_TRAINED_MODEL = 'trained_model.pkl'
MODEL_TRAINER_DIR = 'model_trainer'
MODEL_TRAINER_TRAINED_MODEL_DIR = 'trained_model'
MODEL_TRAINER_EXPECTED_SCORE = 0.6
MODEL_TRAINER_THRESHOLD = 0.05
