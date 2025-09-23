JobHunt Assistant


📌 Overview

JobHunt Assistant automates job searching by:

🔍 Fetching jobs from multiple APIs (Adzuna, Jooble)

📊 Ranking postings by resume keywords

🗂 Tracking applications in Google Sheets

📧 Sending daily email summaries

🎯 A personal job-hunting tool and portfolio project demonstrating Python automation.

🛠 Features

Multi-source job fetching

Keyword-based ranking

Google Sheets integration

Daily email digest

Application status tracking

🏗 Tech Stack

Python 3.10+

Libraries: requests, pandas, gspread, oauth2client

APIs: Adzuna, Jooble, Google Sheets, Gmail

Tools: Git, VS Code, Google Cloud

🖼️ Workflow

flowchart LR
    A[APIs: Adzuna, Jooble] --> F[Fetcher]
    F --> R[Ranker]
    R --> C[CSV]
    C --> GS[Google Sheets]
    C --> E[Email]

📁 Structure

JobHuntAssistant/
├── main.py
├── adzuna.py
├── jooble.py
├── fetch_jobs.py
├── filter_jobs.py
├── save_to_sheets.py
├── send_email.py
├── track_status.py
├── data/
└── config/

▶️ Usage

python main.py

🚀 Future Enhancements

🌐 Web dashboard

🧠 Smarter ranking






