import os
import sys
from source.exception import CustomException
from source.logger import logging

from sklearn.linear_model import LinearRegression,Ridge,Lasso,ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from source.utils.utils import save_object

from dataclasses import dataclass
from source.utils.utils import evaluate_model
@dataclass
class ModelTrainerConfig:
    model_trainer_file_path=os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("initiating model training")
            #seperate dependent and independent features from train and test arrays
            X_train=train_array[:,:-1]
            Y_train=train_array[:,-1]
            X_test=test_array[:,:-1]
            Y_test=test_array[:,-1]

            #crate dict of models
            models={
                'LinearRegression':LinearRegression(),
                'Lasso':Lasso(),
                'Ridge':Ridge(),
                'Elasticnet':ElasticNet(),
                "Decisiontree":DecisionTreeRegressor(),
                "RandomForest":RandomForestRegressor()
            }
            #train and evaluate models with evaluate fucntion from utils
            model_report:dict=evaluate_model(X_train,Y_train,X_test,Y_test,models)
            print(model_report)
            print("="*45)
            logging.info(f"model_reports: {model_report}")

            #to get best model score from dictionsy:
            best_model_score=max(sorted(model_report.values()))

            best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            #get best model
            best_model=models[best_model_name]

            print(f"Best model: {best_model_name}: r2_score: {best_model_score}%")
        
            logging.info(f"Best model: {best_model_name}: r2_score: {round(best_model_score)}%")


            #save model as pickle file
            save_object(
                file_path=self.model_trainer_config.model_trainer_file_path,
                obj=best_model
            )

        except Exception as e:
            logging.info("Error in model model trainer")
            raise CustomException(e,sys)
