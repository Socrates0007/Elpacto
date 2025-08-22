# splitter.py
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from typing import List
from config import CREDS_FILE, MASTER_SHEET_ID, HEADERS, STATE_DIR
from personal_sheets import PEOPLE

TRACK_FILE = os.path.join(STATE_DIR, "last_distributed_row.txt")

def _ensure_state_dir():
    os.makedirs(STATE_DIR, exist_ok=True)

def _load_last_distributed_row() -> int:
    _ensure_state_dir()
    if not os.path.exists(TRACK_FILE):
        return 1  # only header exists (row 1)
    with open(TRACK_FILE, "r") as f:
        s = f.read().strip()
        return int(s) if s.isdigit() else 1

def _save_last_distributed_row(n: int) -> None:
    _ensure_state_dir()
    with open(TRACK_FILE, "w") as f:
        f.write(str(n))

def _gs_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
    return gspread.authorize(creds)

def _ensure_headers(ws):
    if not ws.row_values(1):
        ws.append_row(HEADERS, value_input_option="USER_ENTERED")

def split_new_master_rows_round_robin() -> int:
    client = _gs_client()
    master = client.open_by_key(MASTER_SHEET_ID).sheet1

    all_vals: List[List[str]] = master.get_all_values()
    if not all_vals:
        print("Master is empty.")
        return 0

    header, data = all_vals[0], all_vals[1:]

    last_idx = _load_last_distributed_row()
    # last_idx is the *last* distributed absolute row number.
    # Master data rows start at row 2 => data index 0 == row 2.
    # So new rows are data[(last_idx-1):]
    start_data_index = max(0, last_idx - 1)
    new_rows = data[start_data_index:]

    if not new_rows:
        print("✅ No new rows to distribute.")
        return 0

    # Distribute 1-by-1 across PEOPLE
    assigned_count = 0
    for idx, row in enumerate(new_rows):
        person = PEOPLE[idx % len(PEOPLE)]
        ws = client.open_by_key(person["sheet_id"]).sheet1
        _ensure_headers(ws)
        ws.append_row(row, value_input_option="USER_ENTERED")
        assigned_count += 1
        print(f"✅ Assigned to {person['name']}: {row}")

    # Update tracker to the new last distributed absolute row
    new_last_abs = 1 + len(data)  # header row(1) + count of data rows
    _save_last_distributed_row(new_last_abs)
    print(f"✅ Updated last_distributed_row -> {new_last_abs}")

    return assigned_count

if __name__ == "__main__":
    split_new_master_rows_round_robin()
