"""Split the validated complaints by date received and add the target.
 
train: Jan-Apr 2026 | validate: May | test: 1-23 June | live: from 24 June,
the day the CFPB announced changes to its complaint process.
 
Run from the repo root:  uv run python -m copilot.data.split
"""
 
from pathlib import Path
 
import pandas as pd
 
processed_data = Path(r"C:\Users\nickc\Desktop\Code\Personal Projects\AI\complaint_triage_copilot\src\copilot\data\processed\complaints_2026_valid.parquet")
output_dir = Path("data/processed")
 
EDGES = pd.to_datetime(["2026-01-01", "2026-05-01", "2026-06-01", "2026-06-24", "2027-01-01"])
SPLITS = ["train", "validate", "test", "live"]
MIN_POSITIVES = 300
 
 
def add_target(df: pd.DataFrame) -> pd.DataFrame:
    """1 for monetary relief, 0 for any other closed outcome, missing if not closed yet."""
    response = df["company_response"]
    closed = response.str.startswith("Closed")
    target = response.eq("Closed with monetary relief").astype("Int8").where(closed)
    return df.assign(target=target)
 
 
def assign_split(df: pd.DataFrame) -> pd.DataFrame:
    """Label each row by its date received. Intervals include the start date, not the end."""
    return df.assign(split=pd.cut(df["date_received"], bins=EDGES, right=False, labels=SPLITS))
 
 
def split_complaints(in_path: str | Path = processed_data, out_dir: str | Path = output_dir) -> dict[str, pd.DataFrame]:
    df = assign_split(add_target(pd.read_parquet(in_path)))
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(df)
 
    parts = {}
    for name in SPLITS:
        part = df[df["split"] == name].drop(columns="split")
        if name != "live":
            part = part[part["target"].notna()]  # model building needs a known outcome
        part.to_parquet(out_dir / f"{name}.parquet", index=False)
        parts[name] = part
 
        positives = int(part["target"].sum())
        print(f"{name:>8}: {len(part):>7,} rows, {positives:>5,} positives, base rate {part['target'].mean():.1%}")
        if name in ("validate", "test") and positives < MIN_POSITIVES:
            print(f"          warning: under {MIN_POSITIVES} positives, so metrics on this split will be noisy")
    return parts
 
 
if __name__ == "__main__":
    split_complaints()
 