from src.end_to_end_ds.components.data_transformation import DataTransformation
from src.end_to_end_ds.config.configuration import ConfigurationManager
from src.end_to_end_ds import logger

STAGE_NAME = "DATA TRANSFORMATION STAGE"

class DataTransformationPipeline:
    def __init__(self):
        pass

    def init_data_transformation(self):
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        data_transformation = DataTransformation(data_transformation_config)
        data_transformation.split_data()

def main():
    try:
        logger.info(f">>>>>>>>>>>>>> {STAGE_NAME} started <<<<<<<<<<<<<<")
        obj = DataTransformationPipeline()
        obj.init_data_transformation()
        logger.info(f">>>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<<<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e 


if __name__ == "__main__":
    main()