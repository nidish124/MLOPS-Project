from NetworkSecurity.Components.data_ingestion import DataIngestion
from NetworkSecurity.Entity import artifacts_entity, config_entity
from NetworkSecurity.Execption import execption
from NetworkSecurity.Logging import logger
from NetworkSecurity.Components.data_validation import DataValidation
from NetworkSecurity.Components.data_transformation import DataTransformation
from NetworkSecurity.Components.model_trainer import ModelTrainer
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
        print(Data_ingest_artifact, "data validation its completed")

        data_transformation_config = config_entity.DataTransformationConfig(Training_config)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_tranformation()
        logger.logging.info("Data Transformation Completed")
        print(data_transformation_artifact, "data Transformation its completed")

        model_trainer_config = config_entity.ModelTrainerConfig(Training_config)
        model_trainer = ModelTrainer(data_transformation_artifact, model_trainer_config)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logger.logging.info("Model Trainer is Completed")
        print(data_transformation_artifact, "Model Trainer is Completed")

    except Exception as e:
        raise execption.Custom_execption(e,sys)
