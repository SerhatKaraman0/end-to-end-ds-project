# End-to-End Data Science Project

## Project Overview
This project is an end-to-end data science pipeline designed to automate and modularize the process of data ingestion, processing, and experimentation. It is structured for scalability, reproducibility, and ease of collaboration, using best practices in Python packaging and workflow management.

The repository also ships with a lightweight Flask web UI that lets you run each pipeline stage, view metrics, and make predictions. The homepage shows an interactive Mermaid flowchart of the pipeline with clickable nodes.

Mermaid is pinned to version 10.9.3 for consistent rendering.

## Folder Structure
```
end-to-end-ds/
│
├── config/                # Configuration files (YAML)
│   └── config.yaml        # Main pipeline configuration
├── logs/                  # Log files for tracking pipeline runs
│   └── logging.log        # Main log file
├── research/              # Jupyter notebooks for experimentation
│   ├── 01_data_ingestion.ipynb
│   └── research.ipynb
├── src/end_to_end_ds/     # Main source code package
│   ├── components/        # Pipeline components (e.g., data_ingestion.py)
│   ├── config/            # Configuration management (e.g., configuration.py)
│   ├── constants/         # Project-wide constants
│   ├── entity/            # Data entity definitions (e.g., config_entity.py)
│   ├── pipeline/          # Pipeline orchestration (e.g., data_ingestion.py)
│   └── utils/             # Utility functions (e.g., common.py)
├── templates/             # Web templates (e.g., index.html)
├── Dockerfile             # Docker support for containerization
├── main.py                # Entry point for the project
├── Makefile               # Automation commands
├── params.yaml            # Parameter configuration
├── requirements.txt       # Python dependencies
├── schema.yaml            # Data schema definition
├── setup.py               # Project setup script (for packaging)
└── README.md              # Project documentation
```

## Quickstart
- Ensure you have Python 3.10+ installed.
- Create a virtual environment and install dependencies:
  - macOS/Linux:
    ```bash
    make setup
    ```
  - Or manually:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

### Run the web UI
```bash
make run-ui            # default PORT=5050
```
Navigate to `http://127.0.0.1:5050`.

From the homepage you can:
- Click a stage node in the flowchart to run only that stage.
- Click Run All to execute the full pipeline: ingestion → validation → transformation → training → evaluation.
- View the latest metrics and open MLflow (if configured).
- Go to Predict to make single or batch predictions.

### Run stages from CLI (without UI)
```bash
make run-data-ingestion
make run-data-validation
make run-data-transformation
make run-model-training
make run-model-evaluation
```

## Environment variables
These are optional but recommended. Create a `.env` file in the project root or export the vars in your shell.

- `FLASK_SECRET_KEY`: Secret for Flask sessions. Default: `super-secret-key`.
- `PORT`: Port for the web UI. Default: `5000` (Makefile defaults to 5050).
- `MLFLOW_TRACKING_URI`: MLflow tracking server URI. Example: `https://dagshub.com/<user>/<repo>.mlflow` or a local path like `file:./mlruns`.
- `DAGSHUB_REPO_URL`: Dagshub repository URL if you want auto-MLflow initialization. Example: `https://dagshub.com/<user>/<repo>`.

If both `MLFLOW_TRACKING_URI` and `DAGSHUB_REPO_URL` are present, the app attempts to initialize Dagshub and then log metrics and the model to MLflow.

## Key Components
- **config/config.yaml**: Main configuration for the pipeline, including artifact locations and data sources.
- **params.yaml**: Stores hyperparameters and other adjustable settings.
- **schema.yaml**: Defines the expected data schema.
- **src/end_to_end_ds/components/**: Contains modular pipeline steps (e.g., data ingestion).
- **src/end_to_end_ds/pipeline/**: Orchestrates the execution of pipeline stages.
- **src/end_to_end_ds/utils/common.py**: Utility functions for file I/O, directory management, etc.
- **src/end_to_end_ds/entity/config_entity.py**: Data classes for configuration objects.
- **logs/logging.log**: Centralized logging for debugging and monitoring.
- **research/**: Jupyter notebooks for prototyping and analysis.
- **Makefile**: Automation for setup, cleaning, and running pipeline steps.

## How the web UI works
- Route `/` renders `templates/index.html`, which includes a Mermaid `flowchart LR` showing the stages.
- Each node is clickable and posts to `/run/<stage>`.
- The latest evaluation metrics are read from `artifacts/model_evaluation/metrics.json` and displayed on the right.
- Route `/predict` provides forms for single prediction and CSV batch upload. Outputs are saved to `artifacts/uploads/`.

Mermaid notes:
- Mermaid 10.9.3 is loaded in `templates/base.html`.
- Diagram orientation is left-to-right and nodes are clickable with tooltips.

## Makefile Commands
- `make help` — List all available commands with descriptions.
- `make clean` — Remove the virtual environment and all Python cache files.
- `make setup` — Clean, create a new virtual environment, install dependencies, and run the template script to scaffold files.
- `make install` — Install all dependencies from requirements.txt.
- `make run-data-ingestion` — Run the data ingestion pipeline step.
 - `make run-data-validation` — Run the data validation step.
 - `make run-data-transformation` — Run the data transformation step.
 - `make run-model-training` — Train the model.
 - `make run-model-evaluation` — Evaluate and log metrics/model.
 - `make run-ui` — Start the Flask web UI (`PORT` env var supported).

## How the Pipeline Works
1. **Configuration**: All paths and parameters are managed via YAML files for easy modification.
2. **Data Ingestion**: Downloads and extracts data from a remote source, as defined in `config.yaml`.
3. **Pipeline Orchestration**: Each stage (e.g., ingestion) is modular and can be run independently or as part of a larger workflow.
4. **Logging**: All steps are logged for traceability.
5. **Experimentation**: Notebooks in the `research/` folder allow for rapid prototyping and analysis.

## Getting Started
1. Clone the repository.
2. Run `make setup` to initialize the environment.
3. Start the UI with `make run-ui` or run stages via Make targets.
4. Explore and modify notebooks in the `research/` folder for experimentation.

## Module and function reference (short)

### `src/end_to_end_ds/utils/common.py`
- `read_yaml(path: Path) -> ConfigBox`: Load YAML into a dot-accessible config object. Raises on empty/invalid YAML.
- `create_directories(paths: list[str], verbose=True)`: `os.makedirs(..., exist_ok=True)` for each path; logs creations.
- `save_json(path: Path, data: dict)`: Write JSON with indentation and log location.
- `load_json(path: Path) -> ConfigBox`: Read JSON and return a dot-accessible object.
- `save_bin(data: Any, path: Path)`: Persist a Python object using `joblib.dump`.

### `src/end_to_end_ds/pipeline/data_ingestion.py`
- `DataIngestionPipeline.init_data_ingestion()`: Builds `DataIngestion` from config and runs `download_file()` then `extract_file()`.

### `src/end_to_end_ds/pipeline/data_validation.py`
- `DataValidationPipeline.init_data_validation()`: Builds `DataValidation` and runs `validate_all_columns()` against `schema.yaml`.

### `src/end_to_end_ds/pipeline/data_transformation.py`
- `DataTransformationPipeline.init_data_transformation()`: Ensures validation status is true, then creates `DataTransformation` and runs `split_data()` to create train/test CSVs.

### `src/end_to_end_ds/pipeline/model_trainer.py`
- `ModelTrainingPipeline.init_model_training()`: Creates `ModelTrainer` and runs `train()`; saves model to `artifacts/model_trainer/model.joblib`.

### `src/end_to_end_ds/pipeline/model_evaluation.py`
- `ModelEvaluationPipeline.init_model_evaluation()`: Creates `ModelEvaluation` and runs `log_to_mlflow()` to compute metrics, save them to JSON, and log the model/metrics to MLflow (with Dagshub support when configured).

### `src/end_to_end_ds/pipeline/prediction.py`
- `PredictionPipeline.predict(df: pd.DataFrame) -> np.ndarray`: Loads the trained model and predicts on the provided features.
  - Important: Feature column names in `df` must exactly match the names used during training (as per `schema.yaml`). For CSV batch prediction, ensure headers match the training schema.

## CSV prediction format
The CSV must contain the same feature column names used during training and in `schema.yaml`. For example:
```
fixed acidity,volatile acidity,citric acid,residual sugar,chlorides,free sulfur dioxide,total sulfur dioxide,density,pH,sulphates,alcohol
7.4,0.70,0.00,1.9,0.076,11.0,34.0,0.9978,3.51,0.56,9.4
```
If you use underscores in headers (e.g., `fixed_acidity`), rename them to match the schema (e.g., `fixed acidity`).

## Troubleshooting
- Port already in use: set `PORT=5050` (or another free port) when starting the UI, or use `make run-ui PORT=5050`.
- Mermaid parse error: ensure the first line of the diagram is `flowchart LR` and avoid stray backticks. The app already renders a valid diagram.
- MLflow logging error on Dagshub: some endpoints may be unsupported; the app will fall back to logging the model as an artifact.
- Feature name mismatch during prediction: ensure your input feature names exactly match the training schema (see CSV format above).

## Notes
- The project is designed for extensibility; add new pipeline components as needed.
- Use the Makefile for common tasks to ensure consistency.
- All logs are stored in `logs/logging.log` for easy debugging.

---

For more details, refer to the code and comments in each module.
