import requests
import os

url_val = "http://127.0.0.1:8001/api/upload-and-validate"
url_run = "http://127.0.0.1:8001/api/run-uploaded-investigation"

data_dir = r"e:\KSSEM\CasualCourt_demo_dataset"

files = []
for fname in ["orders.csv", "supplier_events.csv", "inventory.csv", "payments.csv", "tickets.csv"]:
    path = os.path.join(data_dir, fname)
    if os.path.exists(path):
        files.append(('files', (fname, open(path, 'rb'), 'text/csv')))

print("Testing POST /api/upload-and-validate with 5 files (partial data: competitor_prices missing)...")
res_val = requests.post(url_val, files=files)
print(f"Validation Status Code: {res_val.status_code}")
val_data = res_val.json()
print("Validation Output JSON:")
print(val_data)

session_id = val_data.get("session_id")
if session_id:
    print(f"\nTesting POST /api/run-uploaded-investigation with session_id: {session_id}...")
    res_run = requests.post(url_run, json={"session_id": session_id})
    print(f"Run Status Code: {res_run.status_code}")
    run_data = res_run.json()
    print(f"Scenario: {run_data.get('scenario')}")
    print(f"Verdict Primary Cause: {run_data.get('verdict', {}).get('primary_cause')}")
    print(f"Hypotheses count: {len(run_data.get('hypotheses', []))}")
    print("SUCCESSFUL TEST!")
