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

