.PHONY: help clean setup install run-data-ingestion

help: 
	@echo "Available commands"
	@awk 'BEGIN {FS = ":.*?#"} /^[a-zA-Z_-]+:.*?#/ {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean:  # Remove virtual environment and cached files
	rm -rf venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".DS_Store" -delete

setup: clean  # Set up project environment and install dependencies
	python3 -m venv venv
	. venv/bin/activate && \
	pip3 install --upgrade pip && \
	pip3 install -r requirements.txt && \
	python3 template.py 

install: # Install project dependencies 
	pip3 install -r requirements.txt

run-data-ingestion: # Run the Data Ingestion Step in the pipeline 
	source venv/bin/activate && \
	python3 -m src.end_to_end_ds.pipeline.data_ingestion

