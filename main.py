from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Any, List

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory

from src.end_to_end_ds import logger
from src.end_to_end_ds.pipeline.data_ingestion import DataIngestionPipeline
from src.end_to_end_ds.pipeline.data_validation import DataValidationPipeline
from src.end_to_end_ds.pipeline.data_transformation import DataTransformationPipeline
from src.end_to_end_ds.pipeline.model_trainer import ModelTrainingPipeline
from src.end_to_end_ds.pipeline.model_evaluation import ModelEvaluationPipeline
from src.end_to_end_ds.pipeline.prediction import PredictionPipeline
from src.end_to_end_ds.utils.common import read_yaml, create_directories
from src.end_to_end_ds.config.configuration import ConfigurationManager


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-key")
# Dev: disable static caching to reflect CSS changes immediately
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Directories
BASE_DIR = Path(__file__).parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"
UPLOAD_DIR = ARTIFACTS_DIR / "uploads"
create_directories([str(ARTIFACTS_DIR), str(UPLOAD_DIR)])


def get_schema_columns() -> List[str]:
    try:
        schema = read_yaml(Path("schema.yaml"))
        columns = list(schema.COLUMNS.keys())
        target_col = schema.TARGET_COLUMN.name
        return [c for c in columns if c != target_col]
    except Exception:
        # Fallback: try reading transformed train.csv header if exists
        transformed_train = ARTIFACTS_DIR / "data_transformation" / "train.csv"
        if transformed_train.exists():
            import pandas as pd
            cols = list(pd.read_csv(transformed_train, nrows=0).columns)
            if "quality" in cols:
                cols.remove("quality")
            return cols
        return []


def latest_metrics() -> Dict[str, Any]:
    try:
        config = ConfigurationManager().get_model_evaluation_config()
        metrics_path = Path(config.metric_file_name)
        if metrics_path.exists():
            import json
            with open(metrics_path, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


@app.route("/")
def index():
    metrics = latest_metrics()
    mlflow_uri = os.getenv("MLFLOW_TRACKING_URI", "")
    return render_template(
        "index.html",
        metrics=metrics,
        mlflow_uri=mlflow_uri,
    )


@app.route("/run/<stage>", methods=["POST"])
def run_stage(stage: str):
    try:
        if stage == "data_ingestion":
            DataIngestionPipeline().init_data_ingestion()
        elif stage == "data_validation":
            DataValidationPipeline().init_data_validation()
        elif stage == "data_transformation":
            DataTransformationPipeline().init_data_transformation()
        elif stage == "model_training":
            ModelTrainingPipeline().init_model_training()
        elif stage == "model_evaluation":
            ModelEvaluationPipeline().init_model_evaluation()
        elif stage == "all":
            DataIngestionPipeline().init_data_ingestion()
            DataValidationPipeline().init_data_validation()
            DataTransformationPipeline().init_data_transformation()
            ModelTrainingPipeline().init_model_training()
            ModelEvaluationPipeline().init_model_evaluation()
        else:
            flash("Unknown stage", "danger")
            return redirect(url_for("index"))

        flash(f"{stage.replace('_', ' ').title()} completed successfully", "success")
    except Exception as e:
        logger.exception(e)
        flash(f"{stage.replace('_', ' ').title()} failed: {e}", "danger")
    return redirect(url_for("index"))


@app.route("/metrics")
def metrics_page():
    return render_template("metrics.html", metrics=latest_metrics())


@app.route("/predict", methods=["GET", "POST"])
def predict():
    feature_columns = get_schema_columns()
    prediction_result = None
    batch_result_path = None

    if request.method == "POST":
        try:
            predictor = PredictionPipeline()

            if "file" in request.files and request.files["file"].filename:
                uploaded = request.files["file"]
                save_path = UPLOAD_DIR / uploaded.filename
                uploaded.save(save_path)

                import pandas as pd
                df = pd.read_csv(save_path)
                preds = predictor.predict(df)

                df_out = df.copy()
                df_out["prediction"] = preds
                output_path = UPLOAD_DIR / f"predictions_{uploaded.filename}"
                df_out.to_csv(output_path, index=False)
                batch_result_path = output_path.name
                flash("Batch predictions completed", "success")
            else:
                # Single prediction from form
                import pandas as pd
                data = {}
                for col in feature_columns:
                    val = request.form.get(col)
                    if val is None or val == "":
                        raise ValueError(f"Missing value for {col}")
                    try:
                        data[col] = float(val)
                    except ValueError:
                        data[col] = float(val.replace(",", "."))

                df = pd.DataFrame([data])
                pred = predictor.predict(df)[0]
                prediction_result = pred
                flash("Prediction completed", "success")
        except Exception as e:
            logger.exception(e)
            flash(f"Prediction failed: {e}", "danger")

    return render_template(
        "predict.html",
        feature_columns=feature_columns,
        prediction_result=prediction_result,
        batch_result_path=batch_result_path,
    )


@app.route("/downloads/<path:filename>")
def download_file(filename: str):
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
