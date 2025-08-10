import pandas as pd
import numpy as np
import os
import sys
import yaml
from NetworkSecurity.Utils.utils import read_yaml, write_yaml
from NetworkSecurity.Logging.logger import logging
from NetworkSecurity.Execption.execption import Custom_execption
from NetworkSecurity import Constant
from NetworkSecurity.Entity.config_entity import DataIngestionConfig,Training_Pipline_Config,DataValidationConfig
from NetworkSecurity.Entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, 
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.scheme_config = read_yaml(Constant.SCHEMA_FILE_NAME)
        except Exception as e:
            raise Custom_execption(e,sys)
        
    @staticmethod
    def read_csv(file_path) -> pd.DataFrame:
        try:    
            return pd.read_csv(file_path)
        except Exception as e:
            raise Custom_execption(e,sys)
        
    def validate_num_of_columns(self, df:pd.DataFrame) -> bool:
        try:
            self.schema_columns_count = len(self.scheme_config)
            logging.info(f'num of columns mentioned in schema_columns:{self.schema_columns_count}')
            logging.info(f'num of columns in dataframe: {len(df.columns)}')
            if self.schema_columns_count == len(df.columns):
                return True
            return False
        except Exception as e:
            raise Custom_execption(e,sys)
        
    def detect_dataset_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, threashold = 0.5)-> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threashold<= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = True
                report.update({column:{
                    "p-value": float(is_same_dist.pvalue),
                    "drift_status": is_found
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml(file_path = drift_report_file_path,content = report)

        except Exception as e:
            Custom_execption(e,sys)

        
    def initiate_data_validation(self):
        try:
            pass
            self.train_file_path = self.data_ingestion_artifact.trained_file_path
            self.test_file_path  = self.data_ingestion_artifact.test_file_path
            
            self.train_df = DataValidation.read_csv(self.train_file_path)
            self.test_df  = DataValidation.read_csv(self.test_file_path)

            status = self.validate_num_of_columns(df = self.train_df)
            if not status:
                error_message = f"Train dataframe does not contain all columns.\n"
            status = self.validate_num_of_columns(df = self.test_df)
            if not status:
                error_message = f"Train dataframe does not contain all columns.\n"
            
            status = self.detect_dataset_drift(self.train_df,self.test_df)
            
            if not status:
                dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
                os.makedirs(dir_path, exist_ok=True)
                self.train_df.to_csv(
                    self.data_validation_config.valid_train_file_path, index=False, header=True
                )
                
                self.test_df.to_csv(
                    self.data_validation_config.valid_test_file_path, index=False, header=True
                )
            else:
                dir_path = os.path.dirname(self.data_validation_config.invalid_train_file_path)
                os.makedirs(dir_path, exist_ok=True)
                self.train_df.to_csv(
                    self.data_validation_config.invalid_train_file_path, index=False, header=True
                )
                
                self.test_df.to_csv(
                    self.data_validation_config.invalid_test_file_path, index=False, header=True
                )

            data_validation_artifact = DataValidationArtifact(
                 validation_status       = status
                ,valid_train_file_path   = self.data_validation_config.valid_train_file_path
                ,valid_test_file_path    = self.data_validation_config.valid_test_file_path
                ,invalid_train_file_path = self.data_validation_config.invalid_train_file_path
                ,invalid_test_file_path  = self.data_validation_config.invalid_test_file_path
                ,drift_report_file_path  = self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact
        except Exception as e:
            raise Custom_execption(e,sys)

