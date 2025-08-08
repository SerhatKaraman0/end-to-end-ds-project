import os 
import urllib.request as request
import zipfile
from src.end_to_end_ds import logger
from src.end_to_end_ds.entity.config_entity import DataValidationConfig
import pandas as pd

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config 

    
    def validate_all_columns(self) -> bool:
        try:
            validation_status = False

            data = pd.read_csv(self.config.unzip_data_dir)
            all_cols = data.columns

            all_schema = self.config.all_schema.keys()

            for col in all_cols:
                if not col in all_schema:
                    validation_status= False
                    with open(self.config.STATUS_FILE, "w") as file:
                        file.write(f"Validation Status: {validation_status}")
                else:
                    validation_status = True
                    with open(self.config.STATUS_FILE, "w") as file:
                        file.write(f"Validation Status: {validation_status}")

            return validation_status
        
        except Exception as e:
            raise e 


