from fetch_jobs import fetch_all_jobs
from filter_jobs import rank_jobs
from save_to_sheets import upload_jobs_to_sheet
from send_email import send_email

fetch_all_jobs()
rank_jobs()
upload_jobs_to_sheet()
send_email()
