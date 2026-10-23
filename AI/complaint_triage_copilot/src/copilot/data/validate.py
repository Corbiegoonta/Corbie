"""Data contract for the ingested complaints.
 
Cleans the ingested file (redaction tokens, label mapping, duplicates), then
validates it against a pandera schema. Bad data stops the pipeline here,
before it reaches training.
 
Run from the repo root:  uv run python -m copilot.data.validate
"""
 
from pathlib import Path
import pandas as pd
import pandera.pandas as pa

interim_data = Path("interim/complaints_2026.parquet")

interim_output = Path("processed/complaints_2026_valid.parquet")

label_map = Path("C:\\Users\\nickc\\Desktop\\Code\\Personal Projects\\AI\\complaint_triage_copilot\\configs\\label_map_v1.csv")
 
# Replace these with the exact labels from your profile output.
ALLOWED_PRODUCTS = [
    "Checking or savings account",
    "Credit card",
    "Money transfer, virtual currency, or money service",
]
ALLOWED_RESPONSES = [
    "Closed with explanation",
    "Closed with monetary relief",
    "Closed with non-monetary relief",
    "In progress",
    "Untimely response",
]
ALLOWED_TAGS = ["Older American", "Servicemember", "Older American, Servicemember"]
DATE_MIN, DATE_MAX = pd.Timestamp("2026-01-01"), pd.Timestamp("2026-12-31")
 
not_blank = pa.Check(lambda s: s.str.strip().str.len() > 0, error="text is blank")
 
SCHEMA = pa.DataFrameSchema(
    {
        "complaint_id": pa.Column(str, unique=True),
        "date_received": pa.Column("datetime64[ns]", pa.Check.in_range(DATE_MIN, DATE_MAX)),
        "product": pa.Column(str, pa.Check.isin(ALLOWED_PRODUCTS)),
        "sub_product": pa.Column(str, nullable=True),
        "issue": pa.Column(str, not_blank),
        "sub_issue": pa.Column(str, nullable=True),
        "narrative": pa.Column(str, not_blank),
        "company": pa.Column(str, nullable=True),
        "submitted_via": pa.Column(str, nullable=True),
        "tags": pa.Column(str, pa.Check.isin(ALLOWED_TAGS), nullable=True),
        "company_response": pa.Column(str, pa.Check.isin(ALLOWED_RESPONSES)),
    },
    strict=True,
    coerce=True,
)
 
 
def normalise_redactions(text: pd.Series) -> pd.Series:
    """Turn the CFPB's redaction marks into consistent placeholders.
 
    XX/XX/2026 -> [DATE], XXXX -> [REDACTED], {$500.00} -> $500.00
    """
    return (
        text.str.replace(r"\bXX/XX/(?:XXXX|XX|\d{2,4})\b", "[DATE]", regex=True)
        .str.replace(r"\bX{2,}\b", "[REDACTED]", regex=True)
        .str.replace(r"\[REDACTED\](?:\s+\[REDACTED\])+", "[REDACTED]", regex=True)
        .str.replace(r"\{(\$[\d,]+(?:\.\d+)?)\}", r"\1", regex=True)
        .str.strip()
    )
 
 
def dedupe(df: pd.DataFrame) -> pd.DataFrame:
    """Keep one row per complaint ID, preferring a closed record over 'In progress'."""
    still_open = df["company_response"].eq("In progress")
    return (
        df.assign(_open=still_open)
        .sort_values("_open", ascending=False, kind="stable")
        .drop_duplicates("complaint_id", keep="last")
        .drop(columns="_open")
        .sort_index()
    )
 
 
def load_label_map(path: Path = label_map) -> pd.DataFrame:
    """Read the versioned mapping table: column, raw_label, canonical_label."""
    return pd.read_csv(path, dtype=str)
 
 
def apply_label_map(df: pd.DataFrame, label_map: pd.DataFrame) -> pd.DataFrame:
    """Rename old labels to their current name; labels not in the table are unchanged."""
    df = df.copy()
    for column, rows in label_map.groupby("column"):
        df[column] = df[column].replace(dict(zip(rows["raw_label"], rows["canonical_label"])))
    return df
 
 
def find_label_changes(df: pd.DataFrame, column: str, min_rows: int = 50) -> pd.DataFrame:
    """List labels that start after the data begins or stop before it ends.
 
    A label that stops in the same month another starts is probably a rename:
    add it to the mapping table.
    """
    months = df["date_received"].dt.to_period("M")
    spans = (
        df.assign(month=months)
        .groupby(column)["month"]
        .agg(first="min", last="max", rows="size")
        .query("rows >= @min_rows")
    )
    changed = (spans["first"] > months.min()) | (spans["last"] < months.max())
    return spans[changed].sort_values("first")
 
 
def validate_complaints(df: pd.DataFrame) -> pd.DataFrame:
    """Check the data against the contract and report every failure at once."""
    return SCHEMA.validate(df, lazy=True)
 
 
def main() -> None:
    raw = pd.read_parquet(interim_data)
    df = raw.assign(narrative=normalise_redactions(raw["narrative"]))
    df = apply_label_map(df, load_label_map())
    df = dedupe(df)

    for column in ["product", "issue"]:
        changes = find_label_changes(df, column)
        if not changes.empty:
            print(f"Labels in '{column}' that start or stop part-way through:\n{changes}\n")

    try:
        valid = validate_complaints(df)
    except pa.errors.SchemaErrors as err:
        print(err.failure_cases[["column", "check", "failure_case"]].head(20).to_string())
        raise SystemExit("Data contract failed: fix the data or update the contract.") from None

    interim_output.parent.mkdir(parents=True, exist_ok=True)
    valid.to_parquet(interim_output, index=False)
    print(f"{len(raw):,} rows in, {len(raw) - len(df):,} duplicates removed, {len(valid):,} valid rows written to {interim_output}")
 
 
if __name__ == "__main__":
    main()
 