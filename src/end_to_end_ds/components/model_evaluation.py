from src.end_to_end_ds import logger
from src.end_to_end_ds.entity.config_entity import ModelEvaluationConfig
import pandas as pd
import joblib
import dagshub
import os
from dotenv import load_dotenv
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
from src.end_to_end_ds.utils.common import save_json
from pathlib import Path

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config 
    
    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae  = mean_absolute_error(actual, pred)
        r2   = r2_score(actual, pred)

        return rmse, mae, r2
    
    def log_to_mlflow(self):
        try:
            load_dotenv()
            dagshub_url = os.getenv('DAGSHUB_REPO_URL')
            if not dagshub_url:
                mlflow_uri = os.getenv('MLFLOW_TRACKING_URI')
                if mlflow_uri and 'dagshub.com' in mlflow_uri:
                    dagshub_url = mlflow_uri.replace('.mlflow', '')
            
            if dagshub_url:
                dagshub.init(url=dagshub_url, mlflow=True)
                logger.info(f"DagHub initialized with URL: {dagshub_url}")
            else:
                logger.info("No DagHub URL found, using default MLflow configuration")
        except Exception as e:
            logger.warning(f"DagHub initialization failed: {e}. Continuing with local MLflow...")

        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        test_x = test_data.drop(self.config.target_column, axis=1)
        test_y = test_data[[self.config.target_column]]

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        
        with mlflow.start_run():
            predicted_qualities = model.predict(test_x)

            (rmse, mae, r2) = self.eval_metrics(test_y, predicted_qualities)

            scores = {
                "rmse"      : float(rmse),
                "mae"       : float(mae),
                "r2_score"  : float(r2)
            }

            save_json(path=Path(self.config.metric_file_name), data=scores)

            mlflow.log_params(self.config.all_params)
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("mae", mae)
            mlflow.log_metric("r2_score", r2)

            model_logged = False
            
            try:
                if tracking_url_type_store != "file":
                    mlflow.sklearn.log_model(
                        sk_model=model, 
                        artifact_path="model",
                        registered_model_name="ElasticNetWineQuality"
                    )
                else:
                    mlflow.sklearn.log_model(sk_model=model, artifact_path="model")
                model_logged = True
                logger.info("Model logged successfully using mlflow.sklearn.log_model")
            except Exception as e:
                logger.warning(f"Standard model logging failed: {e}")
            
            if not model_logged:
                try:
                    # Log the joblib model file as an artifact
                    mlflow.log_artifact(self.config.model_path, "model")
                    model_logged = True
                    logger.info("Model logged successfully as artifact")
                except Exception as e:
                    logger.warning(f"Artifact logging failed: {e}")
            
            if not model_logged:
                try:
                    import tempfile
                    import pickle
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as tmp_file:
                        pickle.dump(model, tmp_file)
                        tmp_file.flush()
                        mlflow.log_artifact(tmp_file.name, "model")
                        os.unlink(tmp_file.name)  # Clean up temp file
                    model_logged = True
                    logger.info("Model logged successfully as pickle artifact")
                except Exception as e:
                    logger.warning(f"Pickle artifact logging failed: {e}")
            
            if model_logged:
                logger.info("Model successfully logged to MLflow")
            else:
                logger.error("All model logging approaches failed. Model is still available locally.")
            
            logger.info("Model metrics and parameters logged to MLflow successfully")