# master_sheet_updater.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timezone
from typing import List, Dict, Any
from config import CREDS_FILE, MASTER_SHEET_ID, HEADERS
from woo_connector import fetch_new_orders

def _gs_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
    return gspread.authorize(creds)

def _ensure_headers(worksheet):
    first = worksheet.row_values(1)
    if not first:
        worksheet.append_row(HEADERS, value_input_option="USER_ENTERED")

def _fmt_date_gmt(dateStr: str) -> str:
    # Woo gives like "2025-08-20T14:21:33Z"
    # Make YYYY-MM-DD
    if dateStr.endswith("Z"):
        dateStr = dateStr.replace("Z", "+00:00")
    dt = datetime.fromisoformat(dateStr)
    return dt.date().isoformat()

def _orders_to_rows(orders: List[Dict[str, Any]]) -> List[List[str]]:
    rows: List[List[str]] = []
    for o in orders:
        order_date = _fmt_date_gmt(o.get("date_created_gmt", o.get("date_created")))
        order_id = str(o.get("id", ""))
        status = o.get("status", "")
        billing = o.get("billing", {}) or {}
        first = billing.get("first_name", "")
        last = billing.get("last_name", "")
        phone = billing.get("phone", "")
        email = billing.get("email", "")
        address = billing.get("address_1", "")
        city = billing.get("city", "")
        state = billing.get("state", "")
        payment_method = o.get("payment_method_title", "")
        order_total = o.get("total", "")

        line_items = o.get("line_items", []) or []
        if not line_items:
            # still record an empty product row to preserve visibility
            rows.append([
                order_date, order_id, first, last,f"{city}, {state}" ,"","",
                phone
            ])
            continue

        for li in line_items:
            product = li.get("name", "")
            qty = str(li.get("quantity", ""))
            line_total = li.get("total", "")
            '''rows.append([
                order_date, order_id, status, first, last, phone, email,
                address, city, state, payment_method,
                product, qty, line_total, order_total
            ])'''

            rows.append([order_date, order_id,first, last, f"{city}, {state}", 
            product,qty,order_total,phone
            
             ])
    return rows

def append_new_orders_to_master() -> int:
    orders = fetch_new_orders()
    if not orders:
        print("✅ No new orders to add to Master.")
        return 0

    client = _gs_client()
    ws = client.open_by_key(MASTER_SHEET_ID).sheet1
    _ensure_headers(ws)

    rows = _orders_to_rows(orders)
    if rows:
        ws.append_rows(rows, value_input_option="USER_ENTERED")
        print(f"✅ Added {len(rows)} rows to Master.")
    else:
        print("No line items to add.")

    return len(rows)

if __name__ == "__main__":
    append_new_orders_to_master()
