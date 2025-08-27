import pandas as pd
import numpy as np
import os
import sys
import yaml
from NetworkSecurity.Utils.utils import read_yaml, write_yaml, save_object, numpy_array_load
from NetworkSecurity.Logging.logger import logging
from NetworkSecurity.Execption.execption import Custom_execption
from NetworkSecurity import Constant
from NetworkSecurity.Entity.config_entity import DataIngestionConfig,Training_Pipline_Config,DataValidationConfig, DataTransformationConfig
from NetworkSecurity.Entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from scipy.stats import ks_2samp
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

class DataTransformation():
    def __init__(self, data_validation_artifact: DataValidationArtifact, 
                    data_transformation_config: DataTransformationConfig):
        try:    
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise Custom_execption(e,sys)
    
    @staticmethod
    def read_file(file_path:str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise Custom_execption(e,sys)
        
    def get_data_transform_object(self) -> Pipeline:
        try:
            Knn_imputer: KNNImputer = KNNImputer(**Constant.DATA_TRANSFORMATION_INPUT_PARMS)
            processor:Pipeline = Pipeline([("imputer", Knn_imputer)])
            return processor
        except Exception as e:
            raise Custom_execption(e,sys)

    def initiate_data_tranformation(self):
        try:
            valid_train_file_path = self.data_validation_artifact.valid_train_file_path
            valid_test_file_path = self.data_validation_artifact.valid_train_file_path
            train_df = DataTransformation.read_file(valid_train_file_path)
            test_df  = DataTransformation.read_file(valid_test_file_path)

            input_feature_train_df = train_df.drop(columns=[Constant.TARGET_COLUMN])
            target_feature_train_df = train_df[Constant.TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            input_feature_test_df = test_df.drop(columns=[Constant.TARGET_COLUMN])
            target_feature_test_df = test_df[Constant.TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            preprocessor = self.get_data_transform_object()

            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            data_transformation_obj_path = self.data_transformation_config.data_transformation_obj_file_path
            save_object(data_transformation_obj_path,preprocessor)
            numpy_array_load(train_arr,self.data_transformation_config.data_transformation_train_file_path)
            numpy_array_load(test_arr,self.data_transformation_config.data_transformation_test_file_path)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path = self.data_transformation_config.data_transformation_train_file_path
                ,transformed_test_file_path = self.data_transformation_config.data_transformation_test_file_path
                ,transformed_object_file_path = self.data_transformation_config.data_transformation_obj_file_path
            )

            return data_transformation_artifact
        except Exception as e:
            raise Custom_execption(e,sys)