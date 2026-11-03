.PHONY: data eda mlflow baseline xgboost run_all_models, finalise final compare_models

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

xgboost:
	uv run python -X faulthandler -m models.train_xgboost

run_all_models:
	uv run python -X faulthandler -m models.train_baseline
	uv run python -X faulthandler -m models.train_xgboost --trials 60

compare_models:
	uv run python -m models.compare_models

finalise:
	uv run python -m models.finalise_model

final:
	uv run python -m models.finalise_model --final