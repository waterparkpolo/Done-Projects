import pandas as pd

def load_keywords(file_path="config/keywords.txt"):
    with open(file_path, "r") as f:
        return [line.strip().lower() for line in f.readlines()]

def rank_jobs(csv_file="data/all_jobs.csv", output_file="data/ranked_jobs.csv"):
    df = pd.read_csv(csv_file)
    keywords = load_keywords()

    scores = []
    for _, row in df.iterrows():
        description = str(row.get("title", "")).lower()
        score = sum(1 for kw in keywords if kw in description)
        scores.append(score)

    df["score"] = scores
    df_sorted = df.sort_values(by="score", ascending=False)
    df_sorted.to_csv(output_file, index=False)
    print(f"✅ Ranked jobs saved to {output_file}")

if __name__ == "__main__":
    rank_jobs()
