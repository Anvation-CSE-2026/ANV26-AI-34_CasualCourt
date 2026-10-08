import csv
import os
from collections import Counter, defaultdict

data_dir = r"e:\KSSEM\CasualCourt_demo_dataset"

def inspect_orders():
    path = os.path.join(data_dir, "orders.csv")
    with open(path, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    
    total_rows = len(reader)
    order_ids = [r['order_id'] for r in reader]
    unique_orders = set(order_ids)
    dup_count = total_rows - len(unique_orders)
    
    # Deduplicate by order_id keeping first or checking if duplicate statuses differ
    dedup = {}
    for r in reader:
        oid = r['order_id']
        if oid not in dedup:
            dedup[oid] = r
    
    dates = sorted(list(set(r['date'] for r in dedup.values())))
    print(f"=== ORDERS ===")
    print(f"Total Rows: {total_rows}, Unique Orders: {len(unique_orders)}, Duplicates: {dup_count}")
    print(f"Date range: {dates[0]} to {dates[-1]} ({len(dates)} days)")
    
    # Daily cancellation rates
    daily_stats = defaultdict(lambda: {"total": 0, "cancelled": 0, "by_supplier": defaultdict(lambda: {"total": 0, "cancelled": 0})})
    for r in dedup.values():
        d = r['date']
        sup = r['supplier_id']
        daily_stats[d]["total"] += 1
        daily_stats[d]["by_supplier"][sup]["total"] += 1
        if r['status'] == 'Cancelled':
            daily_stats[d]["cancelled"] += 1
            daily_stats[d]["by_supplier"][sup]["cancelled"] += 1

    print("\nSample Daily Cancellation Rates:")
    for d in dates[:10]:
        t = daily_stats[d]["total"]
        c = daily_stats[d]["cancelled"]
        r = c / t if t > 0 else 0
        print(f"Day {d}: {c}/{t} ({r:.2%})")

    print("\nLate Period Sample (Days 35-50 relative to start):")
    for i, d in enumerate(dates):
        t = daily_stats[d]["total"]
        c = daily_stats[d]["cancelled"]
        r = c / t if t > 0 else 0
        sup_str = ", ".join([f"{s}: {daily_stats[d]['by_supplier'][s]['cancelled']}/{daily_stats[d]['by_supplier'][s]['total']}" for s in sorted(daily_stats[d]["by_supplier"].keys())])
        print(f"Day {i+1} ({d}): {c}/{t} ({r:.1%}) -> By Sup: {sup_str}")

def inspect_suppliers():
    path = os.path.join(data_dir, "supplier_events.csv")
    with open(path, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    print("\n=== SUPPLIER EVENTS ===")
    by_sup = defaultdict(list)
    for r in reader:
        by_sup[r['supplier_id']].append((r['date'], float(r['lead_time_days'])))
    
    for sup, vals in sorted(by_sup.items()):
        vals.sort()
        early_avg = sum(v[1] for v in vals[:20]) / 20 if len(vals) >= 20 else 0
        late_avg = sum(v[1] for v in vals[40:50]) / 10 if len(vals) >= 50 else 0
        print(f"{sup}: Early avg lead time = {early_avg:.2f}d, Late avg lead time = {late_avg:.2f}d")

def inspect_inventory():
    path = os.path.join(data_dir, "inventory.csv")
    with open(path, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    print("\n=== INVENTORY ===")
    by_sku = defaultdict(list)
    for r in reader:
        by_sku[r['sku']].append((r['date'], int(r['stock_level'])))
    for sku, vals in sorted(by_sku.items()):
        vals.sort()
        early_avg = sum(v[1] for v in vals[:20]) / 20
        min_val = min(v[1] for v in vals)
        min_date = [v[0] for v in vals if v[1] == min_val][0]
        print(f"{sku}: Early avg stock = {early_avg:.1f}, Min stock = {min_val} at {min_date}")

def inspect_payments():
    path = os.path.join(data_dir, "payments.csv")
    with open(path, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    print("\n=== PAYMENTS ===")
    statuses = Counter(r['payment_status'] for r in reader)
    print(f"Statuses count: {dict(statuses)}")

def inspect_tickets():
    path = os.path.join(data_dir, "tickets.csv")
    with open(path, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    print("\n=== TICKETS ===")
    cats = Counter(r['category'] for r in reader)
    print(f"Ticket categories: {dict(cats)}")
    dates = sorted(list(set(r['date'] for r in reader)))
    print(f"Ticket date range: {dates[0]} to {dates[-1]}")

def inspect_prices():
    path = os.path.join(data_dir, "competitor_prices.csv")
    with open(path, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    print("\n=== COMPETITOR PRICES ===")
    by_sku = defaultdict(list)
    for r in reader:
        by_sku[r['sku']].append((r['date'], float(r['competitor_price'])))
    for sku, vals in sorted(by_sku.items()):
        vals.sort()
        start_p = vals[0][1]
        end_p = vals[-1][1]
        print(f"{sku}: Start price = {start_p}, End price = {end_p}")

if __name__ == "__main__":
    inspect_orders()
    inspect_suppliers()
    inspect_inventory()
    inspect_payments()
    inspect_tickets()
    inspect_prices()
