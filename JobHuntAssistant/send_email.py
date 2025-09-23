import smtplib
import pandas as pd
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load email credentials
with open("config/config.json") as f:
    creds = json.load(f)["email"]

SENDER = creds["sender"]
PASSWORD = creds["password"]
RECIPIENT = creds["recipient"]

def load_top_jobs(csv_file="data/ranked_jobs.csv", top_n=10):
    df = pd.read_csv(csv_file)
    return df.head(top_n)

def send_email():
    jobs = load_top_jobs()

    # Build email body
    body = ""
    for _, row in jobs.iterrows():
        body += f"📌 {row['title']} at {row['company']}\n{row['url']}\n\n"

    # Email setup
    msg = MIMEMultipart()
    msg["From"] = SENDER
    msg["To"] = RECIPIENT
    msg["Subject"] = "🔥 Daily Top Job Matches"
    msg.attach(MIMEText(body, "plain"))

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())

    print(f"✅ Email sent to {RECIPIENT} with {len(jobs)} jobs")

if __name__ == "__main__":
    send_email()
