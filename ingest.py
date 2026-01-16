import hashlib
import pandas as pd
from pathlib import Path

SALT = "service-pricing-optimizer"

def make_customer_id(raw_name: str) -> str:
    h = hashlib.sha256()
    h.update((raw_name + SALT).encode("utf-8"))
    return h.hexdigest()[:10]

def import_raw_csv(path):
    df = pd.read_csv(path, decimal=",")
    df = df.drop(["Számlázási név", "Sz Gy", "Órák", "Város", "Cím", "Számla email"], axis=1)
    df = df.rename(columns={"Diák": "customer_name", "Óradíj": "price"})
    df["customer_id"] = df["customer_name"].apply(make_customer_id)

    date_cols = [c for c in df.columns if c not in ["customer_id", "customer_name", "price"]]
    df[date_cols] = df[date_cols].apply(pd.to_numeric, errors="coerce")
    
    long_df = df.melt(
        id_vars=["customer_id", "price"],
        value_vars=date_cols,
        var_name="date",
        value_name="hours"
    )
    
    long_df = long_df[long_df["hours"] > 0].copy()

    long_df["date"] = pd.to_datetime(long_df["date"])
    
    return long_df

def import_all(paths):
    dfs = []

    for path in paths:
        df = import_raw_csv("data/raw/" + path)
        dfs.append(df)

    full_df = pd.concat(dfs, ignore_index=True)
    return full_df

paths = ["2023sep-nov.csv", "2023dec.csv",
         "2024Q1.csv", "2024Q2.csv", "2024Q3.csv", "2024Q4.csv",
         "2025Q1.csv", "2025Q2.csv", "2025Q3.csv", "2025Q4.csv"]

full_df = import_all(paths)

out_path = Path("data/processed/events_all.csv")
out_path.parent.mkdir(parents=True, exist_ok=True)

full_df.to_csv(out_path, index=False)