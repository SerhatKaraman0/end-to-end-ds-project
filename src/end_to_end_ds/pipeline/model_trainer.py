from src.end_to_end_ds.components.model_trainer import ModelTrainer
from src.end_to_end_ds.config.configuration import ConfigurationManager
from src.end_to_end_ds import logger

STAGE_NAME = "MODEL TRAIN STAGE"

class ModelTrainingPipeline:
    def __init__(self):
        pass

    def init_model_training(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_train = ModelTrainer(model_trainer_config)
        model_train.train()

def main():
    try:
        logger.info(f">>>>>>>>>>>>>> {STAGE_NAME} started <<<<<<<<<<<<<<")
        obj = ModelTrainingPipeline()
        obj.init_model_training()
        logger.info(f">>>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<<<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e 


if __name__ == "__main__":
    main()