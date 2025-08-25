# run_all.py
from master_sheet_updater import append_new_orders_to_master
from splitter import split_new_master_rows_chunks
from whatsapp_sender import send_new_personal_rows_via_whatsapp

def main():
    added = append_new_orders_to_master()
    if added > 0:
        split_new_master_rows_chunks(

            
        )
        send_new_personal_rows_via_whatsapp()
    else:
        print("Nothing new; skipping split and WhatsApp.")

if __name__ == "__main__":
    main()
