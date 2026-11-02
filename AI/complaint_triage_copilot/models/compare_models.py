"""Paired-bootstrap comparison of the champion and a challenger on the validation month.
 
Loads the latest finished baseline run and the latest finished XGBoost tuning run from
MLflow, scores both models on the same validation rows, and resamples those rows with
replacement many times. For each resample it computes both models' PR-AUC and recall at
the top 20%, and records the difference. The 2.5th and 97.5th percentiles of the
differences form a 95% interval. The decision rule fixed in advance is then applied.
 
The challenger's validation score is the best of many tuning trials, so it is optimistic.
The bootstrap measures sampling noise only, not that selection bias.
 
Run from the repo root, with the MLflow server running:
    uv run python -m copilot.models.compare_models
Options: --resamples 1000 --margin 0.02 --baseline-run-id ... --challenger-run-id ...
"""
 
import argparse
 
import mlflow
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score
from .train_baseline import (
    DATA,
    EXPERIMENT,
    TRACKING_URI,
    check_server,
    features_and_target,
    git_commit,
    load,
    recall_at_top,
    sha256,
)
 
BASELINE_RUN_NAME = "baseline-logreg"
CHALLENGER_RUN_NAME = "xgb-tuning"
RUN_NAME = "compare-models"
MARGIN = 0.02          # minimum PR-AUC gain required to adopt the challenger
RESAMPLES = 1_000
SEED = 0
 
 
def latest_run(experiment_id: str, run_name: str) -> pd.Series:
    """The most recent finished run with this name."""
    runs = mlflow.search_runs(
        experiment_ids=[experiment_id],
        filter_string=f"attributes.run_name = '{run_name}' and attributes.status = 'FINISHED'",
        order_by=["attributes.start_time DESC"],
        max_results=1,
    )
    if runs.empty:
        raise SystemExit(f"No finished run named '{run_name}' in experiment '{EXPERIMENT}'.")
    return runs.iloc[0]
 
 
def get_run(experiment_id: str, run_id: str | None, run_name: str) -> pd.Series:
    if run_id is None:
        return latest_run(experiment_id, run_name)
    runs = mlflow.search_runs(experiment_ids=[experiment_id], filter_string=f"attributes.run_id = '{run_id}'")
    if runs.empty:
        raise SystemExit(f"No run with ID {run_id} in experiment '{EXPERIMENT}'.")
    return runs.iloc[0]
 
 
def check_data(run: pd.Series, label: str, current_hash: str) -> None:
    """Warn if the validation file has changed since the model was trained."""
    logged = run.get("tags.data_validate_sha256")
    if isinstance(logged, str) and logged != current_hash:
        print(f"Warning: validate.parquet has changed since the {label} run was logged.")
 
 
def paired_bootstrap(
    y: np.ndarray, base: np.ndarray, chal: np.ndarray, resamples: int, seed: int
) -> dict[str, np.ndarray]:
    """Differences (challenger minus baseline) on the same resampled rows."""
    rng = np.random.default_rng(seed)
    diffs = {"pr_auc": np.empty(resamples), "recall_at_top_20": np.empty(resamples)}
    for b in range(resamples):
        idx = rng.integers(0, len(y), len(y))  # draw len(y) rows with replacement
        yb = y[idx]
        diffs["pr_auc"][b] = average_precision_score(yb, chal[idx]) - average_precision_score(yb, base[idx])
        diffs["recall_at_top_20"][b] = recall_at_top(yb, chal[idx]) - recall_at_top(yb, base[idx])
    return diffs
 
 
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--resamples", type=int, default=RESAMPLES)
    parser.add_argument("--margin", type=float, default=MARGIN)
    parser.add_argument("--baseline-run-id", default=None)
    parser.add_argument("--challenger-run-id", default=None)
    args = parser.parse_args()
 
    check_server(TRACKING_URI)
    mlflow.set_tracking_uri(TRACKING_URI)
    experiment = mlflow.set_experiment(EXPERIMENT)
 
    baseline_run = get_run(experiment.experiment_id, args.baseline_run_id, BASELINE_RUN_NAME)
    challenger_run = get_run(experiment.experiment_id, args.challenger_run_id, CHALLENGER_RUN_NAME)
 
    validate_hash = sha256(DATA / "validate.parquet")
    check_data(baseline_run, "baseline", validate_hash)
    check_data(challenger_run, "challenger", validate_hash)
 
    X, y = features_and_target(load("validate"))
    base = mlflow.sklearn.load_model(f"runs:/{baseline_run.run_id}/model").predict_proba(X)[:, 1]
    chal = mlflow.sklearn.load_model(f"runs:/{challenger_run.run_id}/model").predict_proba(X)[:, 1]
 
    observed = {
        "pr_auc": (average_precision_score(y, base), average_precision_score(y, chal)),
        "recall_at_top_20": (recall_at_top(y, base), recall_at_top(y, chal)),
    }
    print(f"Bootstrapping {args.resamples:,} resamples of {len(y):,} validation rows ({int(y.sum()):,} relief cases)...")
    diffs = paired_bootstrap(y, base, chal, args.resamples, SEED)
 
    summary = {}
    for metric, (b_value, c_value) in observed.items():
        low, high = np.percentile(diffs[metric], [2.5, 97.5])
        summary[metric] = {
            "baseline": b_value,
            "challenger": c_value,
            "difference": c_value - b_value,
            "ci_low": low,
            "ci_high": high,
            "share_challenger_better": float((diffs[metric] > 0).mean()),
        }
 
    gain = summary["pr_auc"]["difference"]
    meets_margin = gain >= args.margin
    excludes_zero = summary["pr_auc"]["ci_low"] > 0
    adopt = meets_margin and excludes_zero
 
    with mlflow.start_run(run_name=RUN_NAME):
        mlflow.log_params(
            {
                "baseline_run_id": baseline_run.run_id,
                "challenger_run_id": challenger_run.run_id,
                "resamples": args.resamples,
                "margin": args.margin,
                "seed": SEED,
            }
        )
        for metric, values in summary.items():
            mlflow.log_metrics({f"{metric}_{k}": v for k, v in values.items()})
        mlflow.set_tags(
            {"decision": "adopt challenger" if adopt else "keep baseline", "git_commit": git_commit(),
             "data_validate_sha256": validate_hash}
        )
        mlflow.log_text(pd.DataFrame(diffs).to_csv(index=False), "bootstrap_differences.csv")
 
    print(f"\n{'metric':<17} {'baseline':>9} {'challenger':>11} {'difference':>11} {'95% interval':>18} {'challenger better':>18}")
    for metric, s in summary.items():
        interval = f"[{s['ci_low']:+.3f}, {s['ci_high']:+.3f}]"
        print(
            f"{metric:<17} {s['baseline']:>9.3f} {s['challenger']:>11.3f} {s['difference']:>+11.3f} "
            f"{interval:>18} {s['share_challenger_better']:>18.0%}"
        )
    print(f"\nRule: adopt the challenger only if PR-AUC improves by at least {args.margin:.3f} and the 95% interval excludes zero.")
    print(f"  Improvement of at least {args.margin:.3f}: {'yes' if meets_margin else 'no'} ({gain:+.3f})")
    print(f"  Interval excludes zero:          {'yes' if excludes_zero else 'no'}")
    print(f"Decision: {'adopt the challenger' if adopt else 'keep the baseline'}.")
 
 
if __name__ == "__main__":
    main()