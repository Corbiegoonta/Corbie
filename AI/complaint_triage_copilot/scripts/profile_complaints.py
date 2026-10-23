"""Quick profile of the ingested complaints, to decide the data contract and splits.
 
Run from the repo root:  uv run python scripts/profile_complaints.py
"""
 
import pandas as pd
 
df = pd.read_parquet(r"C:\Users\nickc\Desktop\Code\Personal Projects\AI\complaint_triage_copilot\src\copilot\data\interim\complaints_2026_validation.parquet")
closed = df["company_response"].ne("In progress")
relief = df["company_response"].eq("Closed with monetary relief")
 
first, last = df["date_received"].min(), df["date_received"].max()
print(f"{len(df):,} rows received {first:%d %b %Y} to {last:%d %b %Y}")
print(f"Duplicate complaint IDs: {df['complaint_id'].duplicated().sum():,}")
 
print("\nShare missing per column:")
print(df.isna().mean().round(3).sort_values(ascending=False).to_string())
 
for column in ["product", "sub_product", "issue", "submitted_via", "company_response", "tags"]:
    print(f"\n{column} (top 10):")
    print(df[column].value_counts(dropna=False).head(10).to_string())
 
# lengths = df["narrative"].str.len()
# print(
#     f"\nNarrative length in characters: median {lengths.median():,.0f}, "
#     f"95th percentile {lengths.quantile(0.95):,.0f}, under 100: {(lengths < 100).mean():.1%}"
# )
print(f"Monetary relief rate among closed cases: {relief[closed].mean():.1%}")
 
monthly = df.assign(
    month=df["date_received"].dt.to_period("M"),
    in_progress=~closed,
    relief_rate=relief.astype(float).where(closed),
)
print("\nBy month:")
print(
    monthly.groupby("month")
    .agg(rows=("complaint_id", "size"), in_progress=("in_progress", "mean"), relief_rate=("relief_rate", "mean"))
    .round(3)
    .to_string()
)
 
