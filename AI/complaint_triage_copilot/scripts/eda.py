"""Exploratory analysis of the split complaints data.
 
Prints tables to the terminal and saves charts to reports/eda/.
Run from the repo root after ingest, validate and split:
 
    uv run python scripts/eda.py
 
Sections 3-6 use the training split only, so every decision comes from
training data and the test set stays untouched.
"""
 
import sys
import textwrap
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt 
import pandas as pd  
from matplotlib.ticker import PercentFormatter  

 
matplotlib.use("Agg")  # write charts to files instead of opening windows
 
DATA = Path("C:\\Users\\nickc\\Desktop\\Code\\Personal Projects\\AI\\complaint_triage_copilot\\src\\copilot\\data\\data\\processed")
OUT = Path("reports/eda")
SPLITS = ["train", "validate", "test", "live"]
CFPB_CHANGE = pd.Timestamp("2026-06-24")
 
BLUE, INK, MUTED, GRID, SURFACE = "#2a78d6", "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "axes.edgecolor": GRID,
    "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.grid": True, "axes.axisbelow": True, "grid.color": GRID, "grid.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlecolor": INK, "axes.titlelocation": "left",
})
pd.set_option("display.width", 140)
pd.set_option("display.max_colwidth", 60)
 
 
def section(title: str) -> None:
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")
 
 
def pct(df: pd.DataFrame, *columns: str) -> pd.DataFrame:
    """Copy of a table with the given columns shown as percentages."""
    out = df.copy()
    for column in columns:
        out[column] = out[column].map(lambda v: f"{v:.1%}" if pd.notna(v) else "")
    return out
 
 
def rate_by(df: pd.DataFrame, column: str, min_rows: int = 50) -> pd.DataFrame:
    """Base rate per category, keeping categories with enough rows to trust."""
    out = df.groupby(column).agg(rows=("target", "size"), base_rate=("target", "mean"))
    return out[out["rows"] >= min_rows].sort_values("base_rate")
 
 
def save(fig: plt.Figure, name: str) -> None:
    path = OUT / name
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\nChart saved: {path}")
 
 
def bar_rates(table: pd.DataFrame, title: str, overall: float, name: str) -> None:
    labels = [textwrap.fill(str(label), 40) for label in table.index]
    fig, ax = plt.subplots(figsize=(8, 0.45 * len(table) + 1.2))
    ax.barh(labels, table["base_rate"], color=BLUE, height=0.7, edgecolor=SURFACE, linewidth=2)
    ax.axvline(overall, color=MUTED, linestyle="--", linewidth=1)
    ax.xaxis.set_major_formatter(PercentFormatter(1.0))
    ax.grid(axis="y", visible=False)
    ax.set_title(title)
    ax.set_xlabel("Monetary relief rate (dashed line: overall train rate)")
    save(fig, name)
 
 
def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # narratives can contain any character
    missing = [name for name in SPLITS if not (DATA / f"{name}.parquet").exists()]
    if missing:
        raise SystemExit(f"Missing {missing} in {DATA}. Run ingest, validate and split first.")
    OUT.mkdir(parents=True, exist_ok=True)
 
    splits = {name: pd.read_parquet(DATA / f"{name}.parquet") for name in SPLITS}
    train = splits["train"]
    overall = train["target"].mean()
 
    section("1. Target by split: is the base rate stable, and are there enough positives?")
    by_split = pd.DataFrame.from_dict(
        {
            name: {
                "rows": len(df),
                "positives": int(df["target"].sum()),
                "base_rate": df["target"].mean(),
                "unlabelled": df["target"].isna().mean(),
            }
            for name, df in splits.items()
        },
        orient="index",
    )
    print(pct(by_split, "base_rate", "unlabelled").to_string())
 
    section("2. Base rate by month: steps or trends, especially after 24 June")
    everything = pd.concat(splits.values(), ignore_index=True)
    monthly = (
        everything.assign(month=everything["date_received"].dt.to_period("M"))
        .groupby("month")
        .agg(
            rows=("complaint_id", "size"),
            base_rate=("target", "mean"),
            unlabelled=("target", lambda s: s.isna().mean()),
        )
    )
    print(pct(monthly, "base_rate", "unlabelled").to_string())
    print("Late months are provisional: complaints that are still open have no outcome yet.")
 
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.plot(monthly.index.to_timestamp(), monthly["base_rate"], color=BLUE, linewidth=2, marker="o", markersize=6)
    ax.set_ylim(0, monthly["base_rate"].max() * 1.3)
    ax.axvline(CFPB_CHANGE, color=MUTED, linestyle="--", linewidth=1)
    ax.text(CFPB_CHANGE, ax.get_ylim()[1], " CFPB process change", color=MUTED, va="top", fontsize=9)
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    ax.set_title("Monetary relief rate by month received")
    save(fig, "1_base_rate_by_month.png")
 
    section("3. Base rate by product and issue (train): which categories differ most?")
    products = rate_by(train, "product")
    print(pct(products, "base_rate").to_string())
    bar_rates(products, "Monetary relief rate by product", overall, "2_base_rate_by_product.png")
 
    issues = rate_by(train, "issue")
    largest = issues.nlargest(15, "rows").sort_values("base_rate")
    print("\n" + pct(largest, "base_rate").to_string())
    bar_rates(largest, "Monetary relief rate by issue (15 largest)", overall, "3_base_rate_by_issue.png")
 
    section("4. Narrative length (train): junk, long tail, and link to redress")
    words = train["narrative"].str.split().str.len()
    print(words.describe(percentiles=[0.05, 0.5, 0.95]).round(0).to_string())
    by_length = (
        train.assign(length_band=pd.qcut(words, 5, duplicates="drop"))
        .groupby("length_band", observed=True)
        .agg(rows=("target", "size"), base_rate=("target", "mean"))
    )
    by_length.index = [f"{band.left:.0f}-{band.right:.0f}" for band in by_length.index]
    print("\n" + pct(by_length, "base_rate").to_string())
 
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.bar(by_length.index, by_length["base_rate"], color=BLUE, width=0.7, edgecolor=SURFACE, linewidth=2)
    ax.axhline(overall, color=MUTED, linestyle="--", linewidth=1)
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    ax.grid(axis="x", visible=False)
    ax.set_title("Monetary relief rate by narrative length")
    ax.set_xlabel("Words in narrative (fifths of the data; dashed line: overall train rate)")
    save(fig, "4_base_rate_by_length.png")
 
    section("5. Tags (train): the groups you'll audit for fairness")
    tag_rates = (
        train.assign(tag=train["tags"].fillna("No tag"))
        .groupby("tag")
        .agg(rows=("target", "size"), base_rate=("target", "mean"))
        .sort_values("rows", ascending=False)
    )
    tag_rates["share_of_rows"] = tag_rates["rows"] / len(train)
    print(pct(tag_rates, "base_rate", "share_of_rows").to_string())
 
    section("6. Example complaints (train): read these")
    for label, name in [(1, "MONETARY RELIEF"), (0, "NO MONETARY RELIEF")]:
        print(f"\n--- {name} ---")
        sample = train[train["target"] == label].sample(min(3, int((train["target"] == label).sum())), random_state=0)
        for _, row in sample.iterrows():
            print(f"\n[{row['product']} | {row['issue']}]")
            print(textwrap.fill(row["narrative"][:500], 100))
 
    section("Summary for DECISIONS.md")
    live = splits["live"]["target"]
    print(f"- Base rate: train {overall:.1%}, live {live.mean():.1%} (provisional: {live.isna().mean():.0%} of live still open)")
    print(
        f"- Positives: validate {int(splits['validate']['target'].sum()):,}, "
        f"test {int(splits['test']['target'].sum()):,} (aim for 300+ each)"
    )
    if overall < 0.03:
        print("- Base rate is under 3%: consider widening the target to any relief.")
    print(f"- Highest-relief issues: {', '.join(issues.tail(3).index[::-1])}")
    print(f"- Lowest-relief issues: {', '.join(issues.head(3).index)}")
    print(
        f"- Narrative length: median {words.median():.0f} words, 95th percentile {words.quantile(0.95):.0f}, "
        f"{(words < 20).mean():.1%} under 20 words"
    )
    print("- Tags: " + "; ".join(f"{tag} {row.rows:,} rows, {row.base_rate:.1%}" for tag, row in tag_rates.iterrows()))
    print(f"\nCharts are in {OUT}/")
 
 
if __name__ == "__main__":
    main()
 