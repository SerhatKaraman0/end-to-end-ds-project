from src.end_to_end_ds.components.data_ingestion import DataIngestion
from src.end_to_end_ds.config.configuration import ConfigurationManager
from src.end_to_end_ds import logger


STAGE_NAME = "DATA INGESTION STAGE"

class DataIngestionPipeline:
    def __init__(self):
        pass


    def init_data_ingestion(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_file()


def main():
    try:
        logger.info(f">>>>>>>>>>>>>> {STAGE_NAME} started <<<<<<<<<<<<<<")
        obj = DataIngestionPipeline()
        obj.init_data_ingestion()
        logger.info(f">>>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<<<<<<<<") 
    except Exception as e:
        logger.exception(e)
        raise e 


if __name__ == "__main__":
    main()
