"""Calibrate the champion, choose its operating point, explain it and check fairness.
 
1. Load the latest finished baseline run (the champion) from MLflow.
2. Calibration: fit Platt scaling and isotonic regression on the first half of the validation
   month, compare their Brier scores on the second half, then refit the better one on the
   whole month.
3. Operating point: a capacity threshold (the top 20% of the queue) and a cost threshold
   (missed redress against an unnecessary senior review), both set on calibrated May scores.
4. Explanation: the terms with the largest weights, and per-complaint reason codes
   (weight x feature value for the features present in a complaint).
5. Fairness: selection rate, recall and precision by tag group at the capacity threshold.
6. With --final only: evaluate once on the test month and register the calibrated model
   as "redress-risk" with the alias "champion". Run this once, after every decision is fixed.
 
Run from the repo root, with the MLflow server running:
    uv run python -m copilot.models.finalise_model            # validation only
    uv run python -m copilot.models.finalise_model --final    # once, at the end
Options: --capacity 0.2 --cost-missed 10 --cost-review 1
"""
 
import argparse
 
import matplotlib
 
matplotlib.use("Agg")  # write figures to files instead of opening windows
import matplotlib.pyplot as plt  # noqa: E402
import mlflow  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from mlflow.models import infer_signature  # noqa: E402
from sklearn.calibration import CalibratedClassifierCV, calibration_curve  # noqa: E402
from sklearn.frozen import FrozenEstimator  # noqa: E402
from sklearn.metrics import brier_score_loss  # noqa: E402
from sklearn.pipeline import Pipeline  # noqa: E402
from .compare_models import latest_run  # noqa: E402
from .train_baseline import (  # noqa: E402
    CATEGORIES,
    DATA,
    EXPERIMENT,
    TRACKING_URI,
    check_server,
    evaluate,
    features_and_target,
    git_commit,
    load,
    sha256,
)
 
CHAMPION_RUN_NAME = "baseline-logreg"
RUN_NAME = "champion-calibrated"
REGISTERED_MODEL = "redress-risk"
ALIAS = "champion"
CALIBRATION_METHODS = ["sigmoid", "isotonic"]  # Platt scaling and isotonic regression
MIN_GROUP_RELIEF = 30   # fewer relief cases than this make a group's recall too noisy to compare
TOP_TERMS = 15          # terms listed in each direction for the global explanation
REASONS_PER_CASE = 3    # reason codes returned per complaint
 
# skops refuses these private scikit-learn calibration classes unless they are explicitly trusted.
SKOPS_TRUSTED_TYPES = [
    "sklearn.calibration._CalibratedClassifier",
    "sklearn.calibration._SigmoidCalibration",
]
 
 
def calibrate(model: Pipeline, X: pd.DataFrame, y: np.ndarray, method: str) -> CalibratedClassifierCV:
    """Fit a calibrator on (X, y) without refitting the model itself."""
    return CalibratedClassifierCV(FrozenEstimator(model), method=method).fit(X, y)
 
 
def choose_calibration(model: Pipeline, X: pd.DataFrame, y: np.ndarray, dates: pd.Series) -> tuple[str, dict]:
    """Fit each method on the first half of the month and compare Brier scores on the second half."""
    midpoint = dates.min() + (dates.max() - dates.min()) / 2
    fit, check = (dates < midpoint).to_numpy(), (dates >= midpoint).to_numpy()
    briers = {"uncalibrated": brier_score_loss(y[check], model.predict_proba(X[check])[:, 1])}
    for method in CALIBRATION_METHODS:
        calibrated = calibrate(model, X[fit], y[fit], method)
        briers[method] = brier_score_loss(y[check], calibrated.predict_proba(X[check])[:, 1])
    best = min(CALIBRATION_METHODS, key=briers.get)
    return best, briers
 
 
def operating_point(y: np.ndarray, p: np.ndarray, threshold: float, cost_missed: float, cost_review: float) -> dict:
    flagged = p >= threshold
    tp = int((flagged & (y == 1)).sum())
    fp = int((flagged & (y == 0)).sum())
    fn = int((~flagged & (y == 1)).sum())
    return {
        "threshold": threshold,
        "flagged_share": flagged.mean(),
        "precision": tp / max(tp + fp, 1),
        "recall": tp / max(tp + fn, 1),
        "cost_per_1000": 1000 * (cost_missed * fn + cost_review * fp) / len(y),
    }
 
 
def lowest_cost_threshold(y: np.ndarray, p: np.ndarray, cost_missed: float, cost_review: float) -> float:
    """The threshold on a 0.01 grid with the lowest cost on these data: a check on calibration."""
    grid = np.linspace(0.01, 0.99, 99)
    costs = [operating_point(y, p, t, cost_missed, cost_review)["cost_per_1000"] for t in grid]
    return float(grid[int(np.argmin(costs))])
 
 
def readable(name: str) -> str:
    """'text__unauthorized' -> '"unauthorized"'; 'categories__product_Credit card' -> 'product = Credit card'."""
    group, _, feature = name.partition("__")
    if group == "text":
        return f'"{feature}"'
    for column in CATEGORIES:
        if feature.startswith(f"{column}_"):
            return f"{column} = {feature[len(column) + 1:]}"
    return feature
 
 
def top_terms(model: Pipeline, n: int = TOP_TERMS) -> pd.DataFrame:
    """Features with the largest positive and negative weights."""
    names = model.named_steps["features"].get_feature_names_out()
    weights = model.named_steps["model"].coef_[0]
    order = np.argsort(weights)
    rows = [*order[::-1][:n], *order[:n]]
    return pd.DataFrame(
        {"feature": [readable(names[i]) for i in rows], "weight": weights[rows],
         "direction": ["towards relief"] * n + ["away from relief"] * n}
    )
 
 
def reason_codes(model: Pipeline, X: pd.DataFrame, top: int = REASONS_PER_CASE) -> list[str]:
    """For each complaint, the features present with the largest weight x value contributions."""
    names = model.named_steps["features"].get_feature_names_out()
    weights = model.named_steps["model"].coef_[0]
    contributions = model.named_steps["features"].transform(X).multiply(weights).tocsr()
    codes = []
    for i in range(contributions.shape[0]):
        row = contributions.getrow(i)
        order = np.argsort(row.data)[::-1][:top]
        codes.append("; ".join(f"{readable(names[row.indices[j]])} ({row.data[j]:+.2f})" for j in order if row.data[j] > 0))
    return codes
 
 
def fairness_table(y: np.ndarray, p: np.ndarray, threshold: float, tags: pd.Series) -> pd.DataFrame:
    frame = pd.DataFrame({"group": tags.fillna("No tag").to_numpy(), "y": y, "flagged": p >= threshold})
    frame["caught"] = frame["flagged"] & (frame["y"] == 1)
    table = frame.groupby("group").agg(
        complaints=("y", "size"), relief_cases=("y", "sum"), flagged=("flagged", "sum"), caught=("caught", "sum")
    )
    table["base_rate"] = table["relief_cases"] / table["complaints"]
    table["selection_rate"] = table["flagged"] / table["complaints"]
    table["recall"] = table["caught"] / table["relief_cases"].clip(lower=1)
    table["precision"] = table["caught"] / table["flagged"].clip(lower=1)
    table["reliable"] = table["relief_cases"] >= MIN_GROUP_RELIEF
    return table.sort_values("complaints", ascending=False)
 
 
def recall_gap(table: pd.DataFrame) -> float:
    reliable = table.loc[table["reliable"], "recall"]
    return float(reliable.max() - reliable.min()) if len(reliable) > 1 else float("nan")
 
 
def reliability_figure(y: np.ndarray, before: np.ndarray, after: np.ndarray, method: str) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(5.5, 5))
    ax.plot([0, 1], [0, 1], linestyle="--", color="#8a8a8a", linewidth=1, label="Perfectly calibrated")
    for scores, label, colour in [(before, "Before calibration", "#c2410c"), (after, f"After ({method})", "#2a78d6")]:
        observed, predicted = calibration_curve(y, scores, n_bins=10, strategy="quantile")
        ax.plot(predicted, observed, marker="o", color=colour, linewidth=2, label=label)
    ax.set_xlabel("Mean predicted probability (each point is one tenth of complaints)")
    ax.set_ylabel("Observed relief rate")
    ax.set_title("Reliability diagram, validation month", loc="left", fontweight="bold")
    ax.legend(frameon=False)
    ax.grid(alpha=0.3)
    return fig
 
 
def print_table(title: str, table: pd.DataFrame, percent: list[str]) -> None:
    shown = table.copy()
    for column in percent:
        shown[column] = shown[column].map(lambda v: f"{v:.1%}")
    print(f"\n{title}\n{shown.to_string()}")
 
 
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--final", action="store_true", help="evaluate once on test and register the model")
    parser.add_argument("--capacity", type=float, default=0.2, help="share of the queue senior handlers can review")
    parser.add_argument("--cost-missed", type=float, default=10.0, help="cost of a missed relief case")
    parser.add_argument("--cost-review", type=float, default=1.0, help="cost of an unnecessary senior review")
    args = parser.parse_args()
 
    check_server(TRACKING_URI)
    mlflow.set_tracking_uri(TRACKING_URI)
    experiment = mlflow.set_experiment(EXPERIMENT)
 
    champion_run = latest_run(experiment.experiment_id, CHAMPION_RUN_NAME)
    model = mlflow.sklearn.load_model(f"runs:/{champion_run.run_id}/model")
 
    validate = load("validate")
    X_val, y_val = features_and_target(validate)
 
    # 1. Calibration
    method, briers = choose_calibration(model, X_val, y_val, validate["date_received"])
    calibrated = calibrate(model, X_val, y_val, method)
    raw_val = model.predict_proba(X_val)[:, 1]
    p_val = calibrated.predict_proba(X_val)[:, 1]
    val_metrics = evaluate(y_val, p_val)
 
    # 2. Operating point
    costs = (args.cost_missed, args.cost_review)
    t_capacity = float(np.quantile(p_val, 1 - args.capacity))
    t_cost = args.cost_review / (args.cost_review + args.cost_missed)
    t_cost_check = lowest_cost_threshold(y_val, p_val, *costs)
    points = pd.DataFrame(
        {"capacity": operating_point(y_val, p_val, t_capacity, *costs), "cost": operating_point(y_val, p_val, t_cost, *costs)}
    ).T
 
    # 3. Explanation
    terms = top_terms(model)
    top_cases = validate.assign(score=p_val).nlargest(50, "score")
    top_cases = top_cases.assign(reasons=reason_codes(model, features_and_target(top_cases)[0]))
 
    # 4. Fairness at the capacity threshold
    fair_val = fairness_table(y_val, p_val, t_capacity, validate["tags"])
 
    with mlflow.start_run(run_name=RUN_NAME):
        mlflow.log_params(
            {
                "champion_run_id": champion_run.run_id,
                "calibration_method": method,
                "capacity": args.capacity,
                "cost_missed": args.cost_missed,
                "cost_review": args.cost_review,
                "threshold_capacity": round(t_capacity, 4),
                "threshold_cost": round(t_cost, 4),
                "final": args.final,
            }
        )
        mlflow.log_metrics({f"calibration_brier_{k}": v for k, v in briers.items()})
        mlflow.log_metrics({f"validate_{k}": v for k, v in val_metrics.items()})
        mlflow.log_metric("validate_lowest_cost_threshold", t_cost_check)
        for name, row in points.iterrows():
            mlflow.log_metrics({f"validate_{name}_{k}": v for k, v in row.items() if k != "threshold"})
        mlflow.log_metric("validate_recall_gap", recall_gap(fair_val))
        mlflow.set_tags({"git_commit": git_commit(), "data_validate_sha256": sha256(DATA / "validate.parquet")})
        mlflow.log_figure(reliability_figure(y_val, raw_val, p_val, method), "reliability_validate.png")
        mlflow.log_text(terms.to_csv(index=False), "top_terms.csv")
        mlflow.log_text(top_cases[["complaint_id", "score", "target", "reasons"]].to_csv(index=False), "reason_codes_top50.csv")
        mlflow.log_text(fair_val.to_csv(), "fairness_validate.csv")
 
        if args.final:
            test = load("test")
            X_test, y_test = features_and_target(test)
            p_test = calibrated.predict_proba(X_test)[:, 1]
            test_metrics = evaluate(y_test, p_test)
            test_points = pd.DataFrame(
                {"capacity": operating_point(y_test, p_test, t_capacity, *costs),
                 "cost": operating_point(y_test, p_test, t_cost, *costs)}
            ).T
            fair_test = fairness_table(y_test, p_test, t_capacity, test["tags"])
            mlflow.log_metrics({f"test_{k}": v for k, v in test_metrics.items()})
            for name, row in test_points.iterrows():
                mlflow.log_metrics({f"test_{name}_{k}": v for k, v in row.items() if k != "threshold"})
            mlflow.log_metric("test_recall_gap", recall_gap(fair_test))
            mlflow.set_tag("data_test_sha256", sha256(DATA / "test.parquet"))
            mlflow.log_text(fair_test.to_csv(), "fairness_test.csv")
 
        sample = X_val.head(100)
        info = mlflow.sklearn.log_model(
            calibrated,
            name="model",
            signature=infer_signature(sample, calibrated.predict_proba(sample)),
            pyfunc_predict_fn="predict_proba",
            skops_trusted_types=SKOPS_TRUSTED_TYPES,
            registered_model_name=REGISTERED_MODEL if args.final else None,
        )
        if args.final:
            mlflow.MlflowClient().set_registered_model_alias(REGISTERED_MODEL, ALIAS, info.registered_model_version)
 
    # Report
    print(f"Champion: run {champion_run.run_id[:8]} ({CHAMPION_RUN_NAME})")
    print("\nCalibration: Brier score on the second half of the validation month (lower is better)")
    for name, value in briers.items():
        print(f"  {name:<13} {value:.4f}{'   <- chosen' if name == method else ''}")
    print(
        f"\nValidation, calibrated ({method}): PR-AUC {val_metrics['pr_auc']:.3f}, recall@20% {val_metrics['recall_at_top_20']:.1%}, "
        f"Brier {val_metrics['brier']:.3f}, skill {val_metrics['brier_skill']:+.2f}, mean score {val_metrics['mean_score']:.3f} "
        f"vs base rate {val_metrics['base_rate']:.3f}"
    )
    print_table(
        f"Operating points on validation (costs: missed relief = {args.cost_missed:g}, unnecessary review = {args.cost_review:g})",
        points.round({"threshold": 4, "cost_per_1000": 1}), ["flagged_share", "precision", "recall"],
    )
    print(f"Cost threshold from the formula: {t_cost:.3f}; lowest-cost threshold found on the data: {t_cost_check:.2f}")
    print(f"\nTerms pushing towards relief: {', '.join(terms.loc[terms['direction'] == 'towards relief', 'feature'].head(8))}")
    print(f"Terms pushing away from relief: {', '.join(terms.loc[terms['direction'] == 'away from relief', 'feature'].head(8))}")
    print("\nReason codes for the three highest-scored validation complaints:")
    for _, case in top_cases.head(3).iterrows():
        print(f"  {case['complaint_id']}: score {case['score']:.2f}, outcome {'relief' if case['target'] == 1 else 'no relief'}: {case['reasons']}")
    columns = ["complaints", "relief_cases", "base_rate", "selection_rate", "recall", "precision", "reliable"]
    print_table("Fairness on validation at the capacity threshold", fair_val[columns], ["base_rate", "selection_rate", "recall", "precision"])
    print(f"Recall gap between groups with at least {MIN_GROUP_RELIEF} relief cases: {recall_gap(fair_val):.1%}")
 
    if args.final:
        print(
            f"\nTEST (evaluated once): PR-AUC {test_metrics['pr_auc']:.3f}, ROC-AUC {test_metrics['roc_auc']:.3f}, "
            f"recall@20% {test_metrics['recall_at_top_20']:.1%}, Brier {test_metrics['brier']:.3f}, "
            f"skill {test_metrics['brier_skill']:+.2f}"
        )
        print_table("Operating points on test (thresholds fixed on validation)", test_points.round({"threshold": 4, "cost_per_1000": 1}), ["flagged_share", "precision", "recall"])
        print_table("Fairness on test", fair_test[columns], ["base_rate", "selection_rate", "recall", "precision"])
        print(f"\nRegistered {REGISTERED_MODEL} version {info.registered_model_version} with alias '{ALIAS}'.")
    else:
        print("\nTest month not evaluated. When every decision above is final, run once with --final.")
 
 
if __name__ == "__main__":
    main()
 