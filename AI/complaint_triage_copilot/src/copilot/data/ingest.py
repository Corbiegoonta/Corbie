"""Ingest the raw CFPB complaints export.
 
Reads the CSV in chunks, keeps 2026 banking complaints that have a narrative,
renames columns to snake_case and writes one Parquet file for later steps.
 
Run from the repo root:  uv run python -m copilot.data.ingest
"""
 
from pathlib import Path
import pandas as pd

data = [Path("src/copilot/data/raw/CCDB_Export_15_January_2026_through_February_2026.csv"), 
                 Path("src/copilot/data/raw/CCDB_Export_16_March_2026.csv"),
                 Path("src/copilot/data/raw/CCDB_Export_17_April_2026.csv"),
                 Path("src/copilot/data/raw/CCDB_Export_18_May_2026.csv"),
                 Path("src/copilot/data/raw/CCDB_Export_19_June_2026.csv"),
                 Path("src/copilot/data/raw/CCDB_Export_20_July_2026.csv"),
                 Path("src/copilot/data/raw/CCDB_Export_21_August_2026.csv")]

data_output = Path("interim/complaints_2026.parquet")
 
# Raw CFPB header -> our name. Only these columns are read; ZIP code, state and
# post-outcome fields are never loaded (data minimisation and no leakage).
COLUMNS = {
    "Complaint ID": "complaint_id",
    "Date received": "date_received",
    "Product": "product",
    "Sub-product": "sub_product",
    "Issue": "issue",
    "Sub-issue": "sub_issue",
    "Consumer complaint narrative": "narrative",
    "Company": "company",
    "Submitted via": "submitted_via",
    "Tags": "tags",
    "Company response to consumer": "company_response",
}
BANKING_PRODUCTS = "Checking or savings|Credit card|Money transfer"
START_DATE = pd.Timestamp("2026-01-01")
 
 
def _filter_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    """Keep 2026 banking complaints with a non-empty narrative."""
    chunk = chunk.rename(columns=COLUMNS)
    chunk["date_received"] = pd.to_datetime(chunk["date_received"], errors="coerce")
    keep = (
        chunk["product"].str.contains(BANKING_PRODUCTS, case=False, na=False)
        & chunk["narrative"].fillna("").str.strip().ne("")
        & (chunk["date_received"] >= START_DATE)
    )
    return chunk.loc[keep]
 
 
def ingest_complaints_data(
    raw_paths: list[Path],
    out_path: Path,
    chunksize: int = 200_000,
) -> pd.DataFrame:
    """Read the raw export in chunks, filter it and write Parquet."""
    rows_read, kept = 0, []
    for raw_path in raw_paths:
        reader = pd.read_csv(raw_path, usecols=list(COLUMNS), dtype=str, chunksize=chunksize)
        for chunk in reader:
            rows_read += len(chunk)
            kept.append(_filter_chunk(chunk))
    df = pd.concat(kept, ignore_index=True)
 
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)
    print(f"Read {rows_read:,} rows, kept {len(df):,}, wrote {out_path}")
    return df
 
 
if __name__ == "__main__":
    ingest_complaints_data(data, data_output)
    