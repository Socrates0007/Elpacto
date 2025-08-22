# config.py

# WooCommerce
STORE_URL = "https://segnixautos.store"
WOO_CONSUMER_KEY = "ck_3112d0ac2f6285760b50a20f5fb075d2ad38ad43"
WOO_CONSUMER_SECRET = "cs_605db68ad203b842f5413137e6d9971a6d96f01b"

# Google Sheets service account JSON (path on disk)
CREDS_FILE = "alien-oarlock-449902-v6-5e8722c4ea80.json"

# Master Google Sheet ID (the big long ID in the URL)
MASTER_SHEET_ID = "1-DWSjn3Boc1BtdzAKEBmnA6sa6RVEGen9PMGnC2IiHU"

# Common header for master & all personal sheets (must match exactly)
HEADERS = [
    "DATE",            # YYYY-MM-DD (order date, GMT)
    "ORDER NUMBER",        # e.g., 12345 (no # prefix)
    "FIRST NAME",    
    "LAST NAME",
    "LOCATION",
    "PRODUCT",
    "QUANTITY",
    "PRICE",
    "PHONE NUMBER",

]

# State directory (for TXT trackers)
STATE_DIR = "state"

# WhatsApp sending safety delay (seconds) between messages
WHATSAPP_DELAY_SECONDS = 5
