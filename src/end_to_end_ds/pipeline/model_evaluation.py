from src.end_to_end_ds.components.model_evaluation import ModelEvaluation
from src.end_to_end_ds.config.configuration import ConfigurationManager
from src.end_to_end_ds import logger


STAGE_NAME = "MODEL EVALUATION STAGE"

class ModelEvaluationPipeline:
    def __init__(self) -> None:
        pass

    def init_model_evaluation(self):
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_train = ModelEvaluation(model_evaluation_config)
        model_train.log_to_mlflow()

def main():
    try:
        logger.info(f">>>>>>>>>>>>>> {STAGE_NAME} started <<<<<<<<<<<<<<")
        obj = ModelEvaluationPipeline()
        obj.init_model_evaluation()
        logger.info(f">>>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<<<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e 


if __name__ == "__main__":
    main() 