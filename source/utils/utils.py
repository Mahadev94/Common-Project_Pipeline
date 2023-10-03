#which functions may be used more than once those codes/functions written in utils
#utils used for-->to write reusable codes which are used in entire project.

import os
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
import pickle
from source.exception import CustomException
from source.logger import logging

#function to save object as pickle file

def save_object(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj,file_obj)
        
    except Exception as e:
        raise CustomException(e,sys)
    
#creat function to train model and evaluate and return report
def evaluate_model(X_train,Y_train,X_test,Y_test,models):
    try:
        # train_report={}
        test_report={}
        for i in range(len(list(models))):
            model=list(models.values())[i] #get one by one model
            #Train model
            model.fit(X_train,Y_train)

            #make prediction
            #predcting Train data
            # y_train_prediction=model.predict(X_train)
            #Predicting test data
            y_test_prediction=model.predict(X_test)

            #evaluate model-r2 score for test and train data
            # train_model_score=r2_score(Y_train,y_train_prediction)

            test_model_score=r2_score(Y_test,y_test_prediction)

            #updating report
            # train_report[list(models.keys())[i]]=train_model_score
            test_report[list(models.keys())[i]]=test_model_score

        return test_report
            
    except Exception as e:
        logging.info("Erroe in evaluate models")
        raise CustomException(e,sys)
    
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
        
    except Exception as e:
        logging.info("Exception occered in load objet utils function")
        raise CustomException(e,sys)