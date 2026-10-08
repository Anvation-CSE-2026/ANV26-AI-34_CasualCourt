import json
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

from investigation_engine import CasualCourtEngine

def main():
    data_dir = r"e:\KSSEM\CasualCourt_demo_dataset"
    print("=== STARTING CAUSALCOURT INVESTIGATION ENGINE TEST ===")
    print(f"Data Directory: {data_dir}")

    engine = CasualCourtEngine(data_dir)
    result = engine.run_investigation()

    result_json = result.model_dump()
    print("\n=== INVESTIGATION RESULT JSON ===")
    print(json.dumps(result_json, indent=2))
    print("\n=== ENGINE TEST PASSED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
