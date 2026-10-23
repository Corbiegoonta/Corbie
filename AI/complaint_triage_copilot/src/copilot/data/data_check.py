# import pandas as pd

# cols = ["Date received", "Product", "Company response to consumer"]
# df = pd.read_csv(r"C:\Users\nickc\Desktop\Code\Personal Projects\AI\complaint_triage_copilot\src\copilot\data\complaints.csv", usecols=cols, dtype=str)
# df["month"] = pd.to_datetime(df["Date received"], errors="coerce").dt.to_period("M")
# df = df[df["Product"].str.contains("Checking|Credit card|Money transfer", case=False, na=False)]

# resp = df["Company response to consumer"]
# in_progress = resp.eq("In progress")
# summary = df.assign(
#     in_progress=in_progress,
#     relief_rate=resp.eq("Closed with monetary relief").astype(float).where(~in_progress),
# ).groupby("month").agg(
#     in_progress=("in_progress", "mean"),
#     relief_rate=("relief_rate", "mean"),
# )
# print(summary.round(3).to_string())
from pathlib import Path
import pandas as pd
for data in ["raw/CCDB_Export_18_May_2026.csv", 
             "raw/CCDB_Export_17_April_2026.csv",
             "raw/CCDB_Export_16_March_2026.csv",
             "raw/CCDB_Export_15_January_2026_through_February_2026.csv",
             "raw/CCDB_Export_21_August_2026.csv", 
             "raw/CCDB_Export_20_July_2026.csv", 
             "raw/CCDB_Export_19_June_2026.csv"]:
    path = Path(data)
    df = pd.read_csv(path)
    print(len(df), path.name, df["Date received"].min(), df["Date received"].max())