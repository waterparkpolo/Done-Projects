import requests
import pandas as pd
import json

# Load API key from config.json
with open("config/config.json") as f:
    keys = json.load(f)
JOOBLE_API_KEY = keys["jooble"]["api_key"]  # Make sure your config has this

def fetch_jooble_jobs(keyword="junior python", location="usa", page=1, results=20):
    url = f"https://jooble.org/api/{JOOBLE_API_KEY}"
    payload = {
        "keywords": keyword,
        "location": location,
        "page": page
    }

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Error fetching Jooble jobs:", response.status_code)
        return pd.DataFrame()

    data = response.json().get("jobs", [])
    jobs = [
        {
            "title": j.get("title", ""),
            "company": j.get("company", ""),
            "url": j.get("link", "")
        }
        for j in data
    ]

    return pd.DataFrame(jobs)

# Example usage
if __name__ == "__main__":
    df = fetch_jooble_jobs(keyword="junior python", location="remote", page=1, results=20)
    print(df)
