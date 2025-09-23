import pandas as pd
from adzuna import fetch_adzuna_jobs
from jooble import fetch_jooble_jobs

def fetch_all_jobs():
    print("Fetching from Adzuna...")
    adzuna_df = fetch_adzuna_jobs()

    print("Fetching from Jooble...")
    jooble_df = fetch_jooble_jobs()

    # Combine and remove duplicates
    all_jobs = pd.concat([jooble_df, adzuna_df], ignore_index=True)
    all_jobs.drop_duplicates(subset=["url"], inplace=True)

    # Save merged results
    all_jobs.to_csv("data/all_jobs.csv", index=False)
    print(f"✅ Saved {len(all_jobs)} combined jobs to data/all_jobs.csv")

if __name__ == "__main__":
    fetch_all_jobs()
