import pandas as pd
import numpy as np
from pymongo import MongoClient
import os
from NetworkSecurity.Logging.logger import logging
from NetworkSecurity.Execption import execption
from dotenv import load_dotenv
from NetworkSecurity import Constant
from NetworkSecurity.Entity.config_entity import DataIngestionConfig
import sys
from sklearn.model_selection import train_test_split
from NetworkSecurity.Entity import artifacts_entity

load_dotenv()

MONGO_DB_connect = os.getenv("MONGO_DB_URL")

class DataIngestion():
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise execption.Custom_execption(e, sys)
    
    def collection_to_database(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.client = MongoClient(MONGO_DB_connect)
            collection = self.client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns = ["_id"],axis = 1)

            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise execption.Custom_execption(e, sys)

    def export_data_into_feature_store(self,df:pd.DataFrame):
        try:
            feature_store_path = self.data_ingestion_config.feature_store_path
            dir_path = os.path.dirname(feature_store_path)
            os.makedirs(dir_path, exist_ok=True)
            df.to_csv(feature_store_path,index=False,header=True)
            return df
        except Exception as e:
            raise execption.Custom_execption(e, sys)

    def split_data_as_trian_test(self, df:pd.DataFrame):
        try:
            train_set, test_set = train_test_split(df, test_size = self.data_ingestion_config.train_test_split_ratio)
            self.dir_ingest_path = os.path.dirname(self.data_ingestion_config.training_path)
            os.makedirs(self.dir_ingest_path,exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.training_path,index=False,header = True)
            test_set.to_csv(self.data_ingestion_config.testing_path,index=False,header = True)

        except Exception as e:
            raise execption.Custom_execption(e, sys)
        
    def initiate_data_ingestion(self):
        try:
            dataframe = self.collection_to_database()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.split_data_as_trian_test(dataframe)
            dataingestionartifact=artifacts_entity.DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_path,
                                                            test_file_path=self.data_ingestion_config.testing_path)
            return dataingestionartifact
        except Exception as e:
            raise execption.Custom_execption(e, sys)