import requests
import pandas as pd
import json

with open("config/config.json") as f:
    keys = json.load(f)
ADZUNA_APP_ID = keys["adzuna"]["app_id"]
ADZUNA_APP_KEY = keys["adzuna"]["app_key"]

def fetch_adzuna_jobs(keyword="junior python", location="usa", results=20):
    url = f"https://api.adzuna.com/v1/api/jobs/us/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": keyword,
        "where": location,
        "results_per_page": results,
        "content-type": "application/json"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error fetching Adzuna jobs:", response.status_code)
        return pd.DataFrame()

    data = response.json().get("results", [])
    jobs = [{"title": j["title"], "company": j["company"]["display_name"], "url": j["redirect_url"]}
            for j in data]

    return pd.DataFrame(jobs)
