import sys
import os
from source.exception import CustomException
from source.logger import logging

from source.utils.utils import load_object
import pandas as pd
class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            #load preprocessor and model file path
            preprocessor_path=os.path.join("artifacts","preprocessor.pkl")
            model_path=os.path.join("artifacts","model.pkl")
            #load these pickle files from utils funt
            preprocessor=load_object(preprocessor_path)
            model=load_object(model_path)

            #scale data
            scaled_data=preprocessor.transform(features)
            #predict
            pred=model.predict(scaled_data)

            return pred

        except Exception as e:
            logging.info("Eception occured in prediction")
            raise CustomException(e,sys)
#we have to create fetures so crate customdata class

class CustomData:
    def __init__(self,
                  carat:float,
                 depth:float,
                 table:float,
                 x:float,
                 y:float,
                 z:float,
                 cut:str,
                 color:str,
                 clarity:str
                 ):
        self.carat = carat
        self.depth = depth
        self.table = table
        self.x = x
        self.y = y
        self.z = z
        self.cut = cut
        self.color = color
        self.clarity = clarity

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict={
                "carat":[self.carat],
                "depth":[self.depth],
                "table":[self.table],
                "x":[self.x],
                "y":[self.y],
                "z":[self.z],
                "cut":[self.cut],
                "color":[self.color],
                "clarity":[self.clarity]              
                }
            df=pd.DataFrame(custom_data_input_dict)
            logging.info("DF is generated")
            return df
        except Exception as e:
            logging.info("Error occred in  custom data predictionpipeline")
            raise CustomException(e,sys)

