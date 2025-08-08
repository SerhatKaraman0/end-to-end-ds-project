from src.end_to_end_ds.components.data_validation import DataValidation
from src.end_to_end_ds.config.configuration import ConfigurationManager
from src.end_to_end_ds import logger

STAGE_NAME = "DATA VALIDATION STAGE"

class DataValidationPipeline:
    def __init__(self):
        pass

    def init_data_validation(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(data_validation_config)
        data_validation.validate_all_columns()

def main():
    try:
        logger.info(f">>>>>>>>>>>>>> {STAGE_NAME} started <<<<<<<<<<<<<<")
        obj = DataValidationPipeline()
        obj.init_data_validation()
        logger.info(f">>>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<<<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e 


if __name__ == "__main__":
    main()