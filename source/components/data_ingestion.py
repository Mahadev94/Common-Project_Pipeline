import os
import sys
#import logging and exception
from source.logger import logging
from source.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split

from source.components.data_transformation import DataTransformation

#import dataclass
from dataclasses import dataclass

#initializing dataingestion configuration-->creating path in cwdir for train and test data
@dataclass
class DataIngestionconfig:
    train_data_path:str=os.path.join("artifacts","train.csv")
    test_data_path:str=os.path.join("artifacts","test.csv")
    raw_data_path:str=os.path.join("artifacts","raw.csv")

#cretae data ingestion class:
class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionconfig() #creat obj for tarin test file path for dataingestionconfig class

    def initiate_data_ingestion(self):
        logging.info("starting data ingestion")

        try:
            df=pd.read_csv(os.path.join("notebooks/data","train.csv")) #read data
            logging.info("Data is read as pandas df")

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True) #make dir to save data
            df.to_csv(self.ingestion_config.raw_data_path,index=False) #save data as raw data

            logging.info("Traintest split starts")
            train_set,test_set=train_test_split(df,test_size=0.30,random_state=42) #split data into train and test sets

            logging.info("train and test sets save") #save train and test sets to dir
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Data Ingestion completed") #finally return train and test sets
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )


        except Exception as e:
            logging.info("exception occured at data ingestion")
            raise CustomException(e,sys)

