"""XGBoost challenger for the redress-risk model, tuned with Optuna and tracked in MLflow.
 
Same inputs as the baseline. The TF-IDF vocabulary is reduced to the 2,000 terms with the
strongest chi-squared association with the target, so SHAP reason codes come out as
readable words. Class imbalance is handled with scale_pos_weight, the number of trees is
set by early stopping on the validation month, and Optuna searches the other settings to
maximise validation PR-AUC. Each trial is a nested MLflow run under one parent run, and
the best trial's fitted pipeline is logged as the parent run's model.
 
The test split is not used here. It is evaluated once, for the final calibrated model.
 
Run from the repo root, with the MLflow server running:
    uv run python -m copilot.models.train_xgboost --trials 30
"""
 
import argparse
import os
 
import mlflow
import numpy as np
import optuna
from mlflow.models import infer_signature
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier
 
from .train_baseline import (
    CATEGORIES,
    DATA,
    EXPERIMENT,
    ONE_HOT,
    TEXT,
    TFIDF,
    TRACKING_URI,
    check_server,
    evaluate,
    features_and_target,
    git_commit,
    load,
    sha256,
)
 
RUN_NAME = "xgb-tuning"
BASELINE_RUN_NAME = "baseline-logreg"
CHI2_TERMS = 2_000           # TF-IDF terms kept for the model and for SHAP reason codes
N_ESTIMATORS = 2_000         # upper bound on trees; early stopping chooses the actual number
EARLY_STOPPING_ROUNDS = 50   # stop when validation PR-AUC has not improved for this many trees
SEED = 0
 
# name: (type, low, high, log scale). The same dictionary drives the search and is logged.
SEARCH_SPACE = {
    "learning_rate": ("float", 0.01, 0.3, True),
    "max_depth": ("int", 3, 10, False),
    "min_child_weight": ("float", 1.0, 20.0, True),
    "subsample": ("float", 0.5, 1.0, False),
    "colsample_bytree": ("float", 0.3, 1.0, False),
    "reg_lambda": ("float", 1e-3, 10.0, True),
    "reg_alpha": ("float", 1e-3, 10.0, True),
    "gamma": ("float", 0.0, 5.0, False),
}
 
# skops, MLflow's safe model format, refuses these types unless they are explicitly trusted.
SKOPS_TRUSTED_TYPES = [
    "sklearn.feature_selection._univariate_selection.chi2",
    "xgboost.core.Booster",
    "xgboost.sklearn.XGBClassifier",
]
 
os.environ.setdefault("MLFLOW_SUPPRESS_PRINTING_URL_TO_STDOUT", "true")  # one link per trial is noise
 
 
def build_features() -> ColumnTransformer:
    """TF-IDF cut to the CHI2_TERMS terms most associated with relief, plus one-hot categories.
 
    Chi-squared selection uses the labels, so it sits inside the transformer and is fitted
    on training data only.
    """
    text = Pipeline([("tfidf", TfidfVectorizer(**TFIDF)), ("chi2", SelectKBest(chi2, k=CHI2_TERMS))])
    return ColumnTransformer([("text", text, TEXT), ("categories", OneHotEncoder(**ONE_HOT), CATEGORIES)])
 
 
def suggest_params(trial: optuna.Trial) -> dict:
    params = {}
    for name, (kind, low, high, log) in SEARCH_SPACE.items():
        suggest = trial.suggest_int if kind == "int" else trial.suggest_float
        params[name] = suggest(name, low, high, log=log)
    return params
 
 
def make_model(params: dict, scale_pos_weight: float) -> XGBClassifier:
    return XGBClassifier(
        **params,
        n_estimators=N_ESTIMATORS,
        early_stopping_rounds=EARLY_STOPPING_ROUNDS,
        eval_metric="aucpr",
        scale_pos_weight=scale_pos_weight,
        tree_method="hist",
        random_state=SEED,
        n_jobs=-1,
    )
 
 
def baseline_pr_auc(experiment_id: str) -> float | None:
    """Validation PR-AUC of the latest finished baseline run, if there is one."""
    runs = mlflow.search_runs(
        experiment_ids=[experiment_id],
        filter_string=f"attributes.run_name = '{BASELINE_RUN_NAME}' and attributes.status = 'FINISHED'",
        order_by=["attributes.start_time DESC"],
        max_results=1,
    )
    if runs.empty or "metrics.validate_pr_auc" not in runs:
        return None
    return float(runs["metrics.validate_pr_auc"].iloc[0])
 
 
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--trials", type=int, default=30, help="number of Optuna trials")
    args = parser.parse_args()
 
    check_server(TRACKING_URI)
    mlflow.set_tracking_uri(TRACKING_URI)
    experiment = mlflow.set_experiment(EXPERIMENT)
 
    train = load("train")
    X_train, y_train = features_and_target(train)
    X_val, y_val = features_and_target(load("validate"))
    scale_pos_weight = float((y_train == 0).sum() / (y_train == 1).sum())
 
    # The feature step is not tuned, so it is fitted once, on training data, and reused by every trial.
    features = build_features().fit(X_train, y_train)
    F_train, F_val = features.transform(X_train), features.transform(X_val)
    feature_names = features.get_feature_names_out()
 
    best = {"pr_auc": -np.inf, "model": None, "trial": None}
 
    with mlflow.start_run(run_name=RUN_NAME) as parent:
        mlflow.log_params({f"tfidf_{k}": v for k, v in TFIDF.items()})
        mlflow.log_params({f"onehot_{k}": v for k, v in ONE_HOT.items()})
        mlflow.log_params(
            {f"space_{name}": f"{low} to {high}{' (log)' if log else ''}" for name, (_, low, high, log) in SEARCH_SPACE.items()}
        )
        mlflow.log_params(
            {
                "model_type": "XGBClassifier",
                "chi2_terms": CHI2_TERMS,
                "n_features": len(feature_names),
                "n_estimators_max": N_ESTIMATORS,
                "early_stopping_rounds": EARLY_STOPPING_ROUNDS,
                "scale_pos_weight": round(scale_pos_weight, 3),
                "n_trials": args.trials,
                "sampler": "TPE",
                "seed": SEED,
                "train_rows": len(y_train),
                "train_positives": int(y_train.sum()),
                "train_from": str(train["date_received"].min().date()),
                "train_to": str(train["date_received"].max().date()),
            }
        )
        mlflow.set_tags(
            {"git_commit": git_commit(), **{f"data_{s}_sha256": sha256(DATA / f"{s}.parquet") for s in ["train", "validate"]}}
        )
        mlflow.log_text("\n".join(feature_names), "features.txt")
 
        def objective(trial: optuna.Trial) -> float:
            params = suggest_params(trial)
            with mlflow.start_run(run_name=f"trial-{trial.number:02d}", nested=True):
                model = make_model(params, scale_pos_weight)
                model.fit(F_train, y_train, eval_set=[(F_val, y_val)], verbose=False)
                metrics = evaluate(y_val, model.predict_proba(F_val)[:, 1])  # uses the best iteration
                mlflow.log_params(params)
                mlflow.log_metrics({f"validate_{k}": v for k, v in metrics.items()})
                mlflow.log_metric("best_iteration", model.best_iteration)
            if metrics["pr_auc"] > best["pr_auc"]:
                best.update(pr_auc=metrics["pr_auc"], model=model, trial=trial.number)
            return metrics["pr_auc"]
 
        study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=SEED))
        study.optimize(objective, n_trials=args.trials)
 
        # Package the fitted features and the best trial's model as one pipeline.
        pipeline = Pipeline([("features", features), ("model", best["model"])])
        results = evaluate(y_val, pipeline.predict_proba(X_val)[:, 1])
        mlflow.log_params({f"best_{k}": v for k, v in study.best_params.items()} | {"best_trial": best["trial"]})
        mlflow.log_metrics({f"validate_{k}": v for k, v in results.items()})
        mlflow.log_metric("best_iteration", best["model"].best_iteration)
 
        sample = X_train.head(100)
        mlflow.sklearn.log_model(
            pipeline,
            name="model",
            signature=infer_signature(sample, pipeline.predict_proba(sample)),
            input_example=X_train.head(3),
            pyfunc_predict_fn="predict_proba",
            skops_trusted_types=SKOPS_TRUSTED_TYPES,
        )
 
    reference = baseline_pr_auc(experiment.experiment_id)
    print(f"\nBest of {args.trials} trials: trial {best['trial']}, {best['model'].best_iteration + 1} trees")
    print(f"Best settings: {study.best_params}")
    print(f"\n{'model':>10} {'PR-AUC':>8} {'ROC-AUC':>8} {'recall@20%':>11} {'Brier':>7} {'skill':>7}")
    print(
        f"{'xgboost':>10} {results['pr_auc']:>8.3f} {results['roc_auc']:>8.3f} "
        f"{results['recall_at_top_20']:>11.1%} {results['brier']:>7.3f} {results['brier_skill']:>7.2f}"
    )
    if reference is not None:
        print(f"{'baseline':>10} {reference:>8.3f}    (validation PR-AUC difference: {results['pr_auc'] - reference:+.3f})")
    print("\nAll figures are on the validation month. The test split stays untouched until the final model.")
    print(f"Run logged: {TRACKING_URI}/#/experiments/{experiment.experiment_id}/runs/{parent.info.run_id}")
 
 
if __name__ == "__main__":
    main()
 