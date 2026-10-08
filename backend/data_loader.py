import os
import io
import pandas as pd
from typing import Tuple, Dict, Any, List, Optional
from models import DataQualityMetrics

EXPECTED_SCHEMAS = {
    "Orders": {
        "required_columns": ["order_id", "date", "status"],
        "date_columns": ["date", "cancel_date", "promised_date", "delivered_date"],
        "id_column": "order_id"
    },
    "Supplier Events": {
        "required_columns": ["date", "supplier_id", "lead_time_days"],
        "date_columns": ["date"],
        "id_column": "supplier_id",
        "numeric_columns": ["lead_time_days"]
    },
    "Inventory": {
        "required_columns": ["date", "sku", "stock_level"],
        "date_columns": ["date"],
        "id_column": "sku",
        "numeric_columns": ["stock_level"]
    },
    "Payments": {
        "required_columns": ["order_id", "date", "payment_status"],
        "date_columns": ["date"],
        "id_column": "order_id"
    },
    "Support Tickets": {
        "required_columns": ["ticket_id", "order_id", "date", "category"],
        "date_columns": ["date"],
        "id_column": "ticket_id"
    },
    "Competitor Prices": {
        "required_columns": ["date", "sku", "competitor_price"],
        "date_columns": ["date"],
        "id_column": "sku",
        "numeric_columns": ["competitor_price"]
    }
}

class DataLoader:
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = data_dir

    @staticmethod
    def identify_source(filename: str, df: pd.DataFrame) -> Optional[str]:
        cols = set(df.columns.str.strip().str.lower())
        fname = filename.lower()

        if "order_id" in cols and ("status" in cols or "cancel_date" in cols or "orders" in fname):
            return "Orders"
        if "supplier_id" in cols and ("lead_time_days" in cols or "supplier" in fname):
            return "Supplier Events"
        if "stock_level" in cols or ("sku" in cols and "stock_level" in cols or "inventory" in fname):
            return "Inventory"
        if "payment_status" in cols or ("order_id" in cols and "payment_status" in cols or "payments" in fname):
            return "Payments"
        if "ticket_id" in cols or ("category" in cols and "text" in cols or "tickets" in fname):
            return "Support Tickets"
        if "competitor_price" in cols or ("sku" in cols and "competitor_price" in cols or "prices" in fname):
            return "Competitor Prices"

        return None

    @staticmethod
    def validate_file(source_type: str, filename: str, df: pd.DataFrame) -> Tuple[bool, str]:
        if df.empty:
            return False, f"{filename} is empty and contains no rows."

        schema = EXPECTED_SCHEMAS.get(source_type)
        if not schema:
            return False, f"Unknown schema type for {filename}."

        cols = [c.strip().lower() for c in df.columns]
        req_cols = [c.lower() for c in schema["required_columns"]]

        missing = [rc for rc in req_cols if rc not in cols]
        if missing:
            return False, f"{source_type} could not be analyzed because column(s) {', '.join(missing)} are missing in {filename}."

        # Check date parseability
        for date_col in schema.get("date_columns", []):
            matching = [c for c in df.columns if c.strip().lower() == date_col.lower()]
            if matching:
                parsed = pd.to_datetime(df[matching[0]], errors='coerce')
                if parsed.isnull().all():
                    return False, f"{source_type} could not be analyzed because date column '{date_col}' contains invalid or unparseable dates in {filename}."

        # Check numeric parseability
        for num_col in schema.get("numeric_columns", []):
            matching = [c for c in df.columns if c.strip().lower() == num_col.lower()]
            if matching:
                parsed_num = pd.to_numeric(df[matching[0]], errors='coerce')
                if parsed_num.isnull().all():
                    return False, f"{source_type} could not be analyzed because numeric column '{num_col}' contains no valid numbers in {filename}."

        return True, f"{source_type} validated successfully ({len(df)} rows)."

    def process_uploaded_files(self, raw_files: Dict[str, bytes]) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
        recognized = {}
        validation_details = []
        parsed_dfs = {}
        warnings = []
        can_run = False

        for fname, content in raw_files.items():
            if not fname.endswith('.csv'):
                validation_details.append({
                    "filename": fname,
                    "valid": False,
                    "error": f"File {fname} is not a valid CSV file format."
                })
                continue

            try:
                df = pd.read_csv(io.BytesIO(content))
                source = self.identify_source(fname, df)

                if not source:
                    validation_details.append({
                        "filename": fname,
                        "valid": False,
                        "error": f"Could not match schema of {fname} to any recognized CasualCourt business source."
                    })
                    continue

                valid, msg = self.validate_file(source, fname, df)
                if not valid:
                    validation_details.append({
                        "filename": fname,
                        "source": source,
                        "valid": False,
                        "error": msg
                    })
                else:
                    recognized[source] = True
                    validation_details.append({
                        "filename": fname,
                        "source": source,
                        "valid": True,
                        "rows": len(df),
                        "message": msg
                    })
                    parsed_dfs[source] = df
            except Exception as e:
                validation_details.append({
                    "filename": fname,
                    "valid": False,
                    "error": f"Failed to parse CSV {fname}: {str(e)}"
                })

        # Process parsed DataFrames into data_dict
        data_dict = {}
        notes = []

        # Orders is required
        if "Orders" in parsed_dfs:
            df_orders_raw = parsed_dfs["Orders"].copy()
            df_orders_raw['order_id'] = df_orders_raw['order_id'].astype(str).str.strip()
            total_rows = len(df_orders_raw)
            unique_count = df_orders_raw['order_id'].nunique()
            duplicate_count = total_rows - unique_count

            if duplicate_count > 0:
                notes.append(f"Detected {duplicate_count} duplicate order record(s) in uploaded orders. Deduplicating.")

            df_orders = df_orders_raw.drop_duplicates(subset=['order_id'], keep='first').copy()
            for col in ['date', 'cancel_date', 'promised_date', 'delivered_date']:
                if col in df_orders.columns:
                    df_orders[col] = pd.to_datetime(df_orders[col], errors='coerce')
            df_orders['status'] = df_orders['status'].astype(str).str.strip()

            data_dict["orders"] = df_orders
            can_run = True
        else:
            warnings.append("Orders dataset missing. Investigation requires an Orders CSV file.")

        # Supplier Events
        if "Supplier Events" in parsed_dfs:
            df_sup = parsed_dfs["Supplier Events"].copy()
            df_sup['date'] = pd.to_datetime(df_sup['date'], errors='coerce')
            df_sup['supplier_id'] = df_sup['supplier_id'].astype(str).str.strip()
            df_sup['lead_time_days'] = pd.to_numeric(df_sup['lead_time_days'], errors='coerce')
            data_dict["suppliers"] = df_sup
        else:
            data_dict["suppliers"] = None
            warnings.append("Supplier events analysis unavailable (file not uploaded).")

        # Inventory
        if "Inventory" in parsed_dfs:
            df_inv = parsed_dfs["Inventory"].copy()
            df_inv['date'] = pd.to_datetime(df_inv['date'], errors='coerce')
            df_inv['sku'] = df_inv['sku'].astype(str).str.strip()
            df_inv['stock_level'] = pd.to_numeric(df_inv['stock_level'], errors='coerce')
            data_dict["inventory"] = df_inv
        else:
            data_dict["inventory"] = None
            warnings.append("Inventory stock analysis unavailable (file not uploaded).")

        # Payments
        if "Payments" in parsed_dfs:
            df_pay = parsed_dfs["Payments"].copy()
            df_pay['order_id'] = df_pay['order_id'].astype(str).str.strip()
            df_pay['date'] = pd.to_datetime(df_pay['date'], errors='coerce')
            df_pay['payment_status'] = df_pay['payment_status'].astype(str).str.strip()
            data_dict["payments"] = df_pay
        else:
            data_dict["payments"] = None
            warnings.append("Payment gateway analysis unavailable (file not uploaded).")

        # Support Tickets
        if "Support Tickets" in parsed_dfs:
            df_tick = parsed_dfs["Support Tickets"].copy()
            df_tick['ticket_id'] = df_tick['ticket_id'].astype(str).str.strip()
            df_tick['order_id'] = df_tick['order_id'].astype(str).str.strip()
            df_tick['date'] = pd.to_datetime(df_tick['date'], errors='coerce')
            df_tick['category'] = df_tick['category'].astype(str).str.strip()
            data_dict["tickets"] = df_tick
        else:
            data_dict["tickets"] = None
            warnings.append("Support ticket sentiment analysis unavailable (file not uploaded).")

        # Competitor Prices
        if "Competitor Prices" in parsed_dfs:
            df_pr = parsed_dfs["Competitor Prices"].copy()
            df_pr['date'] = pd.to_datetime(df_pr['date'], errors='coerce')
            df_pr['sku'] = df_pr['sku'].astype(str).str.strip()
            df_pr['competitor_price'] = pd.to_numeric(df_pr['competitor_price'], errors='coerce')
            data_dict["prices"] = df_pr
        else:
            data_dict["prices"] = None
            warnings.append("Competitor pricing comparison unavailable (file not uploaded).")

        summary = {
            "can_run": can_run,
            "sources_recognized": {
                "Orders": "Orders" in parsed_dfs,
                "Supplier Events": "Supplier Events" in parsed_dfs,
                "Inventory": "Inventory" in parsed_dfs,
                "Payments": "Payments" in parsed_dfs,
                "Support Tickets": "Support Tickets" in parsed_dfs,
                "Competitor Prices": "Competitor Prices" in parsed_dfs,
            },
            "validation_details": validation_details,
            "warnings": warnings,
            "data_dict": data_dict
        }

        return data_dict, summary

    def load_all_data(self) -> Tuple[Dict[str, pd.DataFrame], DataQualityMetrics]:
        if not self.data_dir:
            raise ValueError("Data directory not set.")

        files = {}
        for fname in ["orders.csv", "supplier_events.csv", "inventory.csv", "payments.csv", "tickets.csv", "competitor_prices.csv"]:
            path = os.path.join(self.data_dir, fname)
            if os.path.exists(path):
                with open(path, "rb") as f:
                    files[fname] = f.read()

        data_dict, summary = self.process_uploaded_files(files)

        orders_df = data_dict.get("orders")
        total_rows = len(orders_df) if orders_df is not None else 0
        unique_count = orders_df['order_id'].nunique() if orders_df is not None else 0
        duplicate_count = total_rows - unique_count

        notes = [v['message'] for v in summary['validation_details'] if v.get('valid')]
        dq = DataQualityMetrics(
            total_order_rows=total_rows,
            unique_order_count=unique_count,
            duplicate_count=duplicate_count,
            data_quality_notes=notes
        )

        return data_dict, dq
