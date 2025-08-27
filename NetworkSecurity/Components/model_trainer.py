import os
import sys 

from NetworkSecurity.Execption.execption import Custom_execption
from NetworkSecurity.Logging.logger import logging

from NetworkSecurity.Entity.artifacts_entity import DataTransformationArtifact, ModelTrainerArtifact
from NetworkSecurity.Entity.config_entity import ModelTrainerConfig

from NetworkSecurity.Utils.ml_utils.estimator import NetworkModel
from NetworkSecurity.Utils.utils import save_object, load_object
from NetworkSecurity.Utils.utils import load_numpy_array_data, evaluate_models
from NetworkSecurity.Utils.ml_utils.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)

class ModelTrainer:
    def __init__(self,data_transformation_artifact: DataTransformationArtifact, 
                    Model_trainer_config: ModelTrainerConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.Model_trainer_config = Model_trainer_config
        except Exception as e:
            raise Custom_execption(e,sys)
        
    def train_model(self,x_train,y_train,x_test,y_test):
        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }

            parms = {
                "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
                },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
                },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
                },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
                }
            }

            model_report:dict = evaluate_models(x_train,y_train,x_test,y_test,
                                                models=models,parms=parms)
            
            best_model_score = max(list(model_report.values()))

            best_model_name = max(model_report, key= model_report.get)

            best_model = models[best_model_name]

            y_train_pred = best_model.predict(x_train)
            classification_training_score = get_classification_score(y_true=y_train, y_pred=y_train_pred)

            y_test_pred = best_model.predict(x_test)
            classification_testing_score = get_classification_score(y_true=y_test, y_pred=y_test_pred)

            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.Model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)

            Network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
            save_object(file_path=self.Model_trainer_config.trained_model_file_path,obj=Network_model)

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path= self.Model_trainer_config.trained_model_file_path,
                                                          train_metric_artifact=classification_training_score,
                                                          test_metric_artifact=classification_testing_score)
            
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        except Exception as e:
            raise Custom_execption(e,sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_array = load_numpy_array_data(train_file_path)
            test_array = load_numpy_array_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1],
            )
            model_trainer_artifact = self.train_model(X_train,y_train,X_test,y_test)
            return model_trainer_artifact

        except Exception as e:
            raise Custom_execption(e,sys)