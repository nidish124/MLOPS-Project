from datetime import datetime
import sys
import os
from NetworkSecurity import Constant
from NetworkSecurity.Logging.logger import logging
from NetworkSecurity.Execption import execption


class Training_Pipline_Config:
    def __init__(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.pipeline_name = Constant.PIPELINE_NAME
        self.artifact_name = Constant.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        self.model_file_path = os.path.dirname(Constant.MODEL_FILE_NAME)
        self.timestamp = timestamp

class DataIngestionConfig():
    def __init__(self,training_pipline_config: Training_Pipline_Config):
        self.data_ingestion_dir:str = os.path.join(
            training_pipline_config.artifact_dir, Constant.DATA_INGESTION_DIRNAME
            )
        self.feature_store_path:str = os.path.join(
            self.data_ingestion_dir, Constant.DATA_INGESTION_FEATURE_STORE_DIR, Constant.FILE_NAME
            )
        self.training_path:str = os.path.join(
            self.data_ingestion_dir, Constant.DATA_INGESTION_INGESTION_DIR, Constant.TRAIN_FILE_NAME
            )
        self.testing_path:str = os.path.join(
            self.data_ingestion_dir, Constant.DATA_INGESTION_INGESTION_DIR, Constant.TEST_FILE_NAME
            )
        self.train_test_split_ratio = Constant.TRAIN_TEST_SPLIT_RATIO
        self.collection_name : str = Constant.COLLECTION_NAME
        self.database_name: str = Constant.DATABASE_NAME

class DataValidationConfig():
    def __init__(self, training_pipline_config: Training_Pipline_Config
                 ):
        self.data_validation_dir :str = os.path.join(
            training_pipline_config.artifact_dir, Constant.DATA_VALIDATION_DIR_NAME
        )
        self.valid_data_path: str = os.path.join(
            self.data_validation_dir,Constant.DATA_VALIDATION_VALID_DIR
        )
        self.invalid_data_path: str = os.path.join(
            self.data_validation_dir,Constant.DATA_VALIDATION_INVALID_DIR
        )
        self.valid_train_file_path: str = os.path.join(
            self.valid_data_path, Constant.TRAIN_FILE_NAME
        )
        self.valid_test_file_path: str = os.path.join(
            self.valid_data_path, Constant.TEST_FILE_NAME
        )
        self.invalid_train_file_path: str = os.path.join(
            self.invalid_data_path, Constant.TRAIN_FILE_NAME
        )
        self.invalid_test_file_path: str = os.path.join(
            self.invalid_data_path, Constant.TEST_FILE_NAME
        )
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            Constant.DATA_VALIDATION_DRIFT_REPORT_DIR,Constant.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )

class DataTransformationConfig():
    def __init__(self, training_pipline_config: Training_Pipline_Config):
        self.data_transformation_dir:str = os.path.join(
            training_pipline_config.artifact_dir, Constant.DATA_TRANSFORMATION_DIR)
        self.data_transformation_train_file_path:str = os.path.join(
            self.data_transformation_dir,Constant.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, 
            Constant.DATA_TRANSFORMATION_TRAIN_FILE
        )
        self.data_transformation_test_file_path:str = os.path.join(
            self.data_transformation_dir,Constant.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, 
            Constant.DATA_TRANSFORMATION_TEST_FILE
        )
        self.data_transformation_obj_file_path:str = os.path.join(
            self.data_transformation_dir,Constant.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            Constant.PREPROCESSING_OBJECT_FILE_NAME
        )

        
class ModelTrainerConfig():
    def __init__(self, training_pipline_config: Training_Pipline_Config):
        self.model_trainer_dir:str = os.path.join(
            training_pipline_config.artifact_dir, Constant.MODEL_TRAINER_DIR)
        
        self.trained_model_file_path:str = os.path.join(
            self.model_trainer_dir,Constant.MODEL_TRAINER_TRAINED_MODEL_DIR, 
            Constant.MODEL_TRAINER_TRAINED_MODEL
        )
        self.expected_accuracy :float = Constant.MODEL_TRAINER_EXPECTED_SCORE
        self.Threshold = Constant.MODEL_TRAINER_THRESHOLD
