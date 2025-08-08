import os 
import urllib.request as request
import zipfile
from src.end_to_end_ds import logger
from src.end_to_end_ds.entity.config_entity import DataTransformationConfig
from sklearn.model_selection import train_test_split
import pandas as pd


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
    
    def split_data(self):
        df = pd.read_csv(self.config.data_path)

        train, test = train_test_split(df, random_state=self.config.random_state)

        train.to_csv(os.path.join(self.config.root_dir, "train.csv"), index=False)
        test.to_csv(os.path.join(self.config.root_dir, "test.csv"), index=False)
        
        logger.info("Split data into train and test sets")
        logger.info(train.shape)
        logger.info(test.shape)

        print(f"Training data shape: {train.shape}")
        print(f"Test data shape: {test.shape}")
