import os
import pandas as pd

data_dir = r"e:\KSSEM\CasualCourt_demo_dataset"

files = ["orders.csv", "supplier_events.csv", "inventory.csv", "payments.csv", "tickets.csv", "competitor_prices.csv"]

print("=== DATA SUMMARY ===")
for f in files:
    path = os.path.join(data_dir, f)
    if os.path.exists(path):
        df = pd.read_csv(path)
        print(f"\n--- {f} ---")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Null count:\n{df.isnull().sum()}")
        print("Sample head:")
        print(df.head(3))
