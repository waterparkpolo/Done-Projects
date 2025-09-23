import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import os

def connect_to_sheet(sheet_name="JobHuntAssistant"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("config/credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1

def upload_jobs_to_sheet(csv_file="data/ranked_jobs.csv", sheet_name="JobHuntAssistant"):
    # Ensure absolute path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, csv_file)

    df = pd.read_csv(csv_path)
    sheet = connect_to_sheet(sheet_name)

    sheet.clear()
    data = [df.columns.tolist()] + df.values.tolist()
    sheet.update("A1", data)

    print(f"✅ Uploaded {len(df)} jobs to Google Sheet: {sheet_name}")

if __name__ == "__main__":
    upload_jobs_to_sheet()
