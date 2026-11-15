"""Evaluate a model within single companies, as a single-firm deployment would see it.

A model trained on complaints about many firms can score well partly by telling the firms
apart, because firms differ in how often they grant relief. A bank deploying the model sees
only its own complaints, so the performance that matters is the ranking within one company.
The script reports three views on the same complaints:

1. Pooled: all complaints together, as in the other scripts.
2. Company only: each complaint scored by its company's relief rate in the training data.
   This benchmark shows how much ranking is possible from knowing the firm alone.
3. Within company: metrics computed separately for each company with enough relief cases,
   then averaged.

ROC-AUC gives the cleanest comparison, because it does not depend on each company's base
rate. If the pooled ROC-AUC is well above the within-company average, part of the model's
performance comes from distinguishing firms rather than complaints.

Run from the repo root, with the MLflow server running:
    uv run python -m copilot.models.evaluate_by_company
Options: --model-uri models:/redress-risk@champion   --split validate|test|live   --min-relief 50
"""

import argparse

import mlflow
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score

from models.train_baseline import EXPERIMENT, TRACKING_URI, check_server, features_and_target, git_commit, load, recall_at_top

RUN_NAME = "evaluate-by-company"
DEFAULT_MODEL_URI = "models:/redress-risk@champion"
MIN_RELIEF = 50      # companies with fewer relief cases give metrics too noisy to report
SHOWN = 15           # companies printed; all are saved to the CSV artifact


def ranking_metrics(y: np.ndarray, scores: np.ndarray) -> dict[str, float]:
    base_rate = y.mean()
    pr_auc = average_precision_score(y, scores)
    return {
        "base_rate": base_rate,
        "pr_auc": pr_auc,
        "pr_auc_lift": pr_auc / base_rate,
        "roc_auc": roc_auc_score(y, scores),
        "recall_at_top_20": recall_at_top(y, scores),
    }


def by_company(frame: pd.DataFrame, min_relief: int) -> pd.DataFrame:
    """Metrics within each company that has at least min_relief relief cases (and some non-relief)."""
    rows = []
    for company, group in frame.groupby("company"):
        relief = int(group["y"].sum())
        if relief < min_relief or relief == len(group):
            continue
        metrics = ranking_metrics(group["y"].to_numpy(), group["score"].to_numpy())
        rows.append({"company": company, "complaints": len(group), "relief_cases": relief, **metrics})
    if not rows:
        raise SystemExit(f"No company has {min_relief} or more relief cases. Lower --min-relief.")
    return pd.DataFrame(rows).set_index("company").sort_values("complaints", ascending=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--model-uri", default=DEFAULT_MODEL_URI)
    parser.add_argument("--split", choices=["validate", "test", "live"], default="validate")
    parser.add_argument("--min-relief", type=int, default=MIN_RELIEF)
    args = parser.parse_args()

    check_server(TRACKING_URI)
    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT)

    data = load(args.split)
    if args.split == "live":
        data = data[data["target"].notna()]  # only complaints whose outcome is known
    X, y = features_and_target(data)
    model = mlflow.sklearn.load_model(args.model_uri)
    frame = pd.DataFrame({"company": data["company"].fillna("Unknown").to_numpy(), "y": y,
                          "score": model.predict_proba(X)[:, 1]})

    # Company-only benchmark: each complaint scored by its company's relief rate in training.
    train = load("train")
    train = train[train["target"].notna()]
    company_rates = train.groupby(train["company"].fillna("Unknown"))["target"].mean().astype(float)
    benchmark = frame["company"].map(company_rates).fillna(float(train["target"].mean())).to_numpy()

    pooled = ranking_metrics(y, frame["score"].to_numpy())
    company_only = ranking_metrics(y, benchmark)
    table = by_company(frame, args.min_relief)
    weights = table["complaints"] / table["complaints"].sum()
    within = {m: float((table[m] * weights).sum()) for m in ["pr_auc_lift", "roc_auc", "recall_at_top_20"]}
    covered = table["complaints"].sum() / len(frame)

    with mlflow.start_run(run_name=RUN_NAME):
        mlflow.log_params({"model_uri": args.model_uri, "split": args.split, "min_relief": args.min_relief,
                           "companies_evaluated": len(table)})
        mlflow.log_metrics({f"pooled_{k}": v for k, v in pooled.items()})
        mlflow.log_metrics({f"company_only_{k}": v for k, v in company_only.items()})
        mlflow.log_metrics({f"within_{k}": v for k, v in within.items()} | {"within_share_of_complaints": covered})
        mlflow.set_tag("git_commit", git_commit())
        mlflow.log_text(table.to_csv(), f"by_company_{args.split}.csv")

    if args.split == "test":
        print("Note: this is a further look at the test month.")
    print(f"Model {args.model_uri} on {args.split}: {len(frame):,} complaints, {int(y.sum()):,} relief cases ({y.mean():.1%})\n")
    print(f"{'view':<34} {'PR-AUC lift':>11} {'ROC-AUC':>8} {'recall@20%':>11}")
    for label, m in [("Pooled (model)", pooled), ("Company only (benchmark)", company_only),
                     (f"Within company (weighted average)", within)]:
        print(f"{label:<34} {m['pr_auc_lift']:>10.2f}x {m['roc_auc']:>8.3f} {m['recall_at_top_20']:>11.1%}")
    print(f"\nWithin-company figures cover {len(table)} companies with at least {args.min_relief} relief cases "
          f"({covered:.0%} of complaints).")

    shown = table.head(SHOWN).copy()
    for column in ["base_rate", "recall_at_top_20"]:
        shown[column] = shown[column].map(lambda v: f"{v:.1%}")
    shown["pr_auc_lift"] = shown["pr_auc_lift"].map(lambda v: f"{v:.2f}x")
    print(f"\n{shown[['complaints', 'relief_cases', 'base_rate', 'pr_auc', 'pr_auc_lift', 'roc_auc', 'recall_at_top_20']].round(3).to_string()}")


if __name__ == "__main__":
    main()