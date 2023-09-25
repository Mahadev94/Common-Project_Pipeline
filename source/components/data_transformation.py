#import required libraries

import os
import sys
from source.exception import CustomException
from source.logger import logging

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OrdinalEncoder
from dataclasses import dataclass

from source.utils.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join("artifacts","preprocessor.pkl") #strore pkl file of preprocessor

#initialize data transformation class
class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformation_object(self):
        try:
            logging.info("Data Transformation started")

            #numerical columns and categorial columns:
            numerical_col=['carat', 'depth', 'table', 'x', 'y', 'z']
            categorical_col=['cut', 'color', 'clarity']
            
            #here definging custom ranking for categorical features which are in ranking as per domain knowledge
            cut_categories=['Fair', 'Good', 'Very Good', 'Premium', 'Ideal']
            color_categories=['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories=['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF']

            logging.info("pipeline started:")

            #numerical pipeline
            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )

            #categorical pipeline
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("ordinalencoder",OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories])),
                    ("scaler",StandardScaler())

                ]
            )

            #combine num and cat feat:
            preprocessor=ColumnTransformer([
                ("num_pipeline",num_pipeline,numerical_col),
                ("cat_pipeline",cat_pipeline,categorical_col)
            ])

            return preprocessor
        
            logging.info("pipeline completed:")


        except Exception as e:
            logging.info("error in data transformation class")
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            #reading train and test data
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("train and test data read completed")
            logging.info(f"Train data:\n{train_df.head().to_string()} ")
            logging.info(f"test data:\n {test_df.head().to_string()}")

            #preprocessing object
            preprocessing_obj=self.get_data_transformation_object()
            logging.info("preprocessing object created")

            #seperate independent and dependent features:
            target_column="price"
            drop_columns=[target_column,"id"]

            input_feature_train_df=train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df=train_df[target_column]

            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df=test_df[target_column]

            #transforming input train and test data with preprocessor object
            input_feature_train_array=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_array=preprocessing_obj.transform(input_feature_test_df)

            #concatenate independent and dependet feature for trainand test data
            train_array=np.c_[input_feature_train_array,np.array(target_feature_train_df)]
            test_array=np.c_[input_feature_test_array,np.array(target_feature_test_df)]

            #saving the preprocessing object in pickle file
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            logging.info("preprocessing pickle file saved")

            return (
                train_array,
                test_array,
                self.data_transformation_config.preprocessor_obj_file_path
                )


        except Exception as e:
            logging.info("Error in initate data transformation")
            raise CustomException(e,sys)