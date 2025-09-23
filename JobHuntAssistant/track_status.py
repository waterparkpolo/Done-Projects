import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_sheet(sheet_name="JobHuntAssistant"):
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("config/credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1

def update_status(job_title, new_status):
    sheet = connect_sheet()
    records = sheet.get_all_records()

    for i, row in enumerate(records, start=2):  # Start at row 2 (skip headers)
        if row["title"].lower() == job_title.lower():
            sheet.update_cell(i, 6, new_status)  # Column 6 = Status
            print(f"✅ Updated status for '{job_title}' to '{new_status}'")
            return
    print("⚠️ Job not found.")

if __name__ == "__main__":
    update_status("Junior Python Developer", "Interview Scheduled")
