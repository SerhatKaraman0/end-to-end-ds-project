import os 
import urllib.request as request
import zipfile
from src.end_to_end_ds import logger
from src.end_to_end_ds.entity.config_entity import ModelTrainerConfig
import pandas as pd
from sklearn.linear_model import ElasticNet
import joblib
import dagshub
from dotenv import load_dotenv



class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)

        train_X = train_data.drop(self.config.target_column, axis=1)
        test_X = test_data.drop(self.config.target_column, axis=1)
        
        train_y = train_data[self.config.target_column]
        test_y = test_data[self.config.target_column]

        model = ElasticNet(alpha=self.config.alpha, l1_ratio=self.config.l1_ratio)
        model.fit(train_X, train_y)

        joblib.dump(model, os.path.join(self.config.root_dir, self.config.model_name))

        

