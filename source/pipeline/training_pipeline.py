
import os
import sys

import pandas as pd
from source.exception import CustomException
from source.logger import logging
from source.components.data_ingestion import DataIngestion
from source.components.data_transformation import DataTransformation
from source.components.model_trainer import ModelTrainer

#Run training pipeline

if __name__=="__main__":
    #initialise data ingestion and call data ingestion function
    obj=DataIngestion()
    train_data_path,test_data_path=obj.initiate_data_ingestion()
    #Initialise data transformation class and call initiate data transformation func
    datatransformation=DataTransformation()
    train_array,test_array,_=datatransformation.initiate_data_transformation(train_data_path,test_data_path)
    #similary call model trainer
    model_trainer=ModelTrainer()
    model_trainer.initiate_model_trainer(train_array,test_array)
