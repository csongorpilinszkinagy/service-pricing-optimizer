import hashlib
import pandas as pd
from pathlib import Path

SALT = "service-pricing-optimizer"

def make_customer_id(raw_name: str) -> str:
    h = hashlib.sha256()
    h.update((raw_name + SALT).encode("utf-8"))
    return h.hexdigest()[:10]

folder = Path("data/raw")
dfs = [pd.read_csv(f, decimal=",") for f in folder.glob("*.csv")]
df = pd.concat(dfs, ignore_index=True)

df = df.rename(columns={"Óradíj": "price"})
df["customer_id"] = df["Diák"].apply(make_customer_id)
df = df.drop(["Diák", "Számlázási név", "Sz Gy", "Órák", "Város", "Cím", "Számla email"], axis=1)
df = df.set_index(["customer_id"])

out_path = Path("data/processed/clean_anonymized.csv")
out_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(out_path)