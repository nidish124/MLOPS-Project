from NetworkSecurity.Components.data_ingestion import DataIngestion
from NetworkSecurity.Entity import artifacts_entity, config_entity
from NetworkSecurity.Execption import execption
from NetworkSecurity.Logging import logger
from NetworkSecurity.Components.data_validation import DataValidation
import sys


if __name__ == '__main__':
    try:
        Training_config = config_entity.Training_Pipline_Config()
        data_ingestion_config = config_entity.DataIngestionConfig(Training_config)
        data_ingest = DataIngestion(data_ingestion_config)
        logger.logging.info("initiate the data ingestion")
        Data_ingest_artifact = data_ingest.initiate_data_ingestion()
        logger.logging.info("Data ingestion Config")
        #logger.logging('Came to almost the end. be carefull.')
        print(Data_ingest_artifact, "data ingestion its completed")
        data_validation_config = config_entity.DataValidationConfig(Training_config)
        data_validation = DataValidation(Data_ingest_artifact, data_validation_config)
        logger.logging.info("initiate the data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logger.logging.info("Data validation Completed")

    except Exception as e:
        raise execption.Custom_execption(e,sys)
