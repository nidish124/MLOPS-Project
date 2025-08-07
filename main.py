from NetworkSecurity.Components.data_ingestion import DataIngestion
from NetworkSecurity.Entity import artifacts_entity, config_entity
from NetworkSecurity.Execption import execption
from NetworkSecurity.Logging import logger

import sys


if __name__ == '__main__':
    try:
        Training_config = config_entity.Training_Pipline_Config()
        data_ingestion_config = config_entity.DataIngestionConfig(Training_config)
        data_ingest = DataIngestion(data_ingestion_config)
        Data_ingest_artifact = data_ingest.initiate_data_ingestion()
        #logger.logging('Came to almost the end. be carefull.')
        print(Data_ingest_artifact, "data ingestion its completed")

    except Exception as e:
        raise execption.Custom_execption(e,sys)
