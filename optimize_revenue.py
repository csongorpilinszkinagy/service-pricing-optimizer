import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

df = pd.read_csv("data/processed/long_format.csv", parse_dates=["date"])
df["revenue"] = df["price"] * df["hours"]
df["quarter"] = df["date"].dt.quarter

agg = df.groupby(['customer_id','quarter'], as_index=False).agg(
    total_hours=('hours','sum'),
    total_revenue=('revenue', 'sum'),
)
agg["avg_price"] = agg["total_revenue"] / agg["total_hours"]

Path("pics").mkdir(parents=True, exist_ok=True)

for quarter in range(1, 5):
    quarter_df = agg[agg["quarter"] == quarter]
    prices = quarter_df["avg_price"].values
    revenues = quarter_df["total_revenue"].values

    coeffs = np.polyfit(prices, revenues, 2)
    poly = np.poly1d(coeffs)

    if coeffs[0] > 0: # no model max, get max revenue example
        opt_price = prices[np.argmax(revenues)]
        opt_revenue = max(revenues)
    else:
        opt_price = -coeffs[1] / (2*coeffs[0])
        opt_price = np.clip(opt_price, min(prices), max(prices))
        opt_revenue = poly(opt_price)

    print(f"Optimal price: {opt_price:.0f}")
    print(f"Predicted revenue: {opt_revenue:.0f}")

    plt.figure()
    p_range = np.linspace(min(prices), max(prices), 500)
    plt.scatter(prices, revenues, color='blue', label='Observed revenue')
    plt.plot(p_range, poly(p_range), color='red', label='Quadratic fit')
    plt.axvline(opt_price, color='green', linestyle='--', label=f'Optimal price {opt_price:.0f}')
    plt.xlabel("Price")
    plt.ylabel("Revenue")
    plt.title(f"Q{quarter} Price vs Revenue")
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.savefig(f"pics/Q{quarter}revenue.png")