# 🏷️ Tag Usage Analyzer for HTML Files

This Python script scans a folder of HTML files to analyze the usage of specified tags and produces three detailed reports, including **monthly and per-tag breakdowns based on timestamps**.

---

## 📌 Features

- ✅ Load tags from a simple `tags.ini` file
- ✅ Scan `.html` files for tag usage
- ✅ Parse timestamps like `data-timestamp="YYYY-MM-DDTHH:MM:SSZ"`
- ✅ Generate **3 reports**:
  - Total tag usage
  - Tag usage per file
  - Tag usage per month


---

## 📂 Folder Structure

project/
├── generate_metrics.py # ← this script
├── tags.ini # ← list of tags to search (1 per line)
└── analyst_folder/ # ← all your HTML files go here
├── example1.html
└── example2.html


---

## ⚙️ Setup Instructions

### 1. Prerequisites

- Python 3.6 or higher
- No third-party libraries required

### 2. Add Your Tags

Create a file called `tags.ini` in the root directory. Each line should be one tag:

grc-risk-assessment
grc-tprm
grc-risk-register


### 3. Add Your HTML Files

Place all `.html` files to be scanned inside a folder named `analyst_folder`.

Each HTML file will include timestamps like:

```html
<div data-timestamp="2025-07-15T09:00:00Z">

</div>
4. Run the Script

python generate_metrics.py
📊 Output Reports
After running, the script generates these CSV files:

1. report_overall_popularity.csv
tag	total_usage_count
GRC-soc2	14
GRC_risk	7

Total usage of each tag across all files.

2. report_anaylyst_engagement.csv
filename	tag	usage_count
file1.html	AI	3
file2.html	cloud	1

Shows how often each tag appeared in each file.

3. report_monthly_trend.csv
month	total_tag_usage
2025-06	8
2025-07	12

Total number of tag occurrences in each month, based on timestamps in the HTML.





🧠 How Timestamp Matching Works
The script splits HTML content using data-timestamp="..." markers.

Each tag is only counted in the context of the timestamped HTML it appears in.

If a file contains multiple timestamps, the script tracks tag usage for each timestamp independently.

🔒 Notes
Tag matching is case-sensitive

Only .html files are processed

HTML files without timestamps are excluded from monthly reports

📥 Sample Output
makefile

Saved: report_overall_popularity.csv
Saved: report_analyst_engagement.csv
Saved: report_monthly_trend.csv

👤 Author
Waterparkpolo
Created using Python
