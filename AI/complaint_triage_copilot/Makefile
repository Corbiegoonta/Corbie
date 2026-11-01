.PHONY: data eda mlflow baseline

data:
	uv run python -m src.copilot.data.ingest
	uv run python -m src.copilot.data.validate
	uv run python -m src.copilot.data.split

eda:
	uv run python -m scripts.eda

mlflow:
	uv run mlflow server --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
	
baseline:
	uv run python -X faulthandler -m models.train_baseline