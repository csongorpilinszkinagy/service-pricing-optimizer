import pandas as pd
from pathlib import Path

df = pd.read_csv("data/processed/clean_anonymized.csv")

date_cols = [c for c in df.columns if c not in ["customer_id", "price"]]
df[date_cols] = df[date_cols].apply(pd.to_numeric, errors="coerce")

long_df = df.melt(
    id_vars=["customer_id", "price"],
    value_vars=date_cols,
    var_name="date",
    value_name="hours"
)

long_df = long_df[long_df["hours"] > 0].copy()
long_df["date"] = pd.to_datetime(long_df["date"])

out_path = Path("data/processed/long_format.csv")
out_path.parent.mkdir(parents=True, exist_ok=True)

long_df.to_csv(out_path, index=False)