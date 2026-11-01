"""Baseline redress-risk model, tracked in MLflow.
 
TF-IDF on the narrative plus one-hot product, sub-product, issue and channel,
feeding a class-weighted logistic regression. Trains on the training split,
evaluates out of time on validate and test, and logs parameters, metrics,
data lineage and the fitted pipeline to a local MLflow tracking server.
 
1. Start the server in its own terminal, from the repo root, and leave it running:
       uv run mlflow server --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
2. Train, from the repo root, in a second terminal:
       uv run python -m copilot.models.train_baseline
3. Open http://127.0.0.1:5000 to inspect the run.
"""
 
import hashlib
import os
import subprocess
import urllib.request
from pathlib import Path
import mlflow
import numpy as np
import pandas as pd
from mlflow.models import infer_signature
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score, precision_recall_curve
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
 
DATA = Path("data/processed")
TEXT = "narrative"
CATEGORIES = ["product", "sub_product", "issue", "submitted_via"]
EVAL_SPLITS = ["validate", "test"]
 
TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
EXPERIMENT = "redress-risk"
RUN_NAME = "baseline-logreg"
 
# These settings ensure the same dictionaries build the model and get logged.
TFIDF = {"min_df": 5, "max_features": 50_000, "ngram_range": (1, 2), "sublinear_tf": True}
ONE_HOT = {"handle_unknown": "ignore", "min_frequency": 20}
MODEL = {"C": 1.0, "class_weight": "balanced", "max_iter": 2000}
 
 
def load(name: str) -> pd.DataFrame:
    return pd.read_parquet(DATA / f"{name}.parquet")
 
 
def features_and_target(df: pd.DataFrame) -> tuple[pd.DataFrame, np.ndarray]:
    return df[[TEXT, *CATEGORIES]].fillna(""), df["target"].astype(int).to_numpy()
 
 
def build_pipeline() -> Pipeline:
    """Every step is fitted on training data only, to ensure there are no leaks from validate or test."""
    features = ColumnTransformer(
        [
            ("text", TfidfVectorizer(**TFIDF), TEXT),
            ("categories", OneHotEncoder(**ONE_HOT), CATEGORIES),
        ]
    )
    return Pipeline([("features", features), ("model", LogisticRegression(**MODEL))])
 
 
def recall_at_top(y: np.ndarray, scores: np.ndarray, share: float = 0.2) -> float:
    """Share of all relief cases that land in the top `share` of the queue."""
    flagged = scores >= np.quantile(scores, 1 - share)
    return (flagged & (y == 1)).sum() / (y == 1).sum()
 
 
def evaluate(y: np.ndarray, scores: np.ndarray) -> dict[str, float]:
    base_rate = y.mean()
    brier = brier_score_loss(y, scores)
    reference = base_rate * (1 - base_rate)  # Brier score of predicting the base rate for every complaint
    return {
        "rows": len(y),
        "base_rate": base_rate,
        "pr_auc": average_precision_score(y, scores),
        "roc_auc": roc_auc_score(y, scores),
        "recall_at_top_20": recall_at_top(y, scores),
        "brier": brier,
        "brier_skill": 1 - brier / reference,  # above 0 beats the base rate; below 0 is worse
        "mean_score": scores.mean(),
    }
 
 
def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
 
 
def git_commit() -> str:
    try:
        result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
 
 
def check_server(uri: str) -> None:
    """Fail fast with a clear message, instead of MLflow retrying for minutes."""
    if not uri.startswith("http"):
        return
    try:
        urllib.request.urlopen(f"{uri}/health", timeout=3)
    except OSError:
        raise SystemExit(
            f"No MLflow server at {uri}. Start it first, from the repo root:\n"
            "  uv run mlflow server --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000"
        ) from None
 
 
def main() -> None:
    check_server(TRACKING_URI)
    mlflow.set_tracking_uri(TRACKING_URI)
    experiment = mlflow.set_experiment(EXPERIMENT)
 
    train = load("train")
    X_train, y_train = features_and_target(train)
 
    with mlflow.start_run(run_name=RUN_NAME) as run:
        mlflow.log_params({f"tfidf_{k}": v for k, v in TFIDF.items()})
        mlflow.log_params({f"onehot_{k}": v for k, v in ONE_HOT.items()})
        mlflow.log_params({f"model_{k}": v for k, v in MODEL.items()})
        mlflow.log_params(
            {
                "model_type": "LogisticRegression",
                "text_column": TEXT,
                "categorical_columns": ",".join(CATEGORIES),
                "train_rows": len(y_train),
                "train_positives": int(y_train.sum()),
                "train_from": str(train["date_received"].min().date()),
                "train_to": str(train["date_received"].max().date()),
            }
        )
        mlflow.set_tags(
            {"git_commit": git_commit(), **{f"data_{s}_sha256": sha256(DATA / f"{s}.parquet") for s in ["train", *EVAL_SPLITS]}}
        )
 
        pipeline = build_pipeline().fit(X_train, y_train)
 
        results = {}
        for name in EVAL_SPLITS:
            X, y = features_and_target(load(name))
            results[name] = evaluate(y, pipeline.predict_proba(X)[:, 1])
            mlflow.log_metrics({f"{name}_{metric}": value for metric, value in results[name].items()})
 
        sample = X_train.head(100)
        mlflow.sklearn.log_model(
            pipeline,
            name="model",
            signature=infer_signature(sample, pipeline.predict_proba(sample)),
            input_example=X_train.head(3),
            pyfunc_predict_fn="predict_proba",
        )
 
    print(f"Trained on {len(y_train):,} complaints. A model with no skill scores PR-AUC equal to the base rate.\n")
    print(f"{'split':>9} {'base rate':>10} {'PR-AUC':>8} {'ROC-AUC':>8} {'recall@20%':>11} {'Brier':>7} {'skill':>7}")
    for name, r in results.items():
        print(
            f"{name:>9} {r['base_rate']:>10.1%} {r['pr_auc']:>8.3f} {r['roc_auc']:>8.3f} "
            f"{r['recall_at_top_20']:>11.1%} {r['brier']:>7.3f} {r['brier_skill']:>7.2f}"
        )
    print(f"\nRun logged: {TRACKING_URI}/#/experiments/{experiment.experiment_id}/runs/{run.info.run_id}")
 
 
if __name__ == "__main__":
    main()