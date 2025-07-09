import os
import csv
import re
from collections import defaultdict

# Load tags from tags.ini
def load_tags(tags_file):
    try:
        with open(tags_file, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {tags_file} not found.")
        return []

# Parse timestamped sections and assign tag counts per month
def count_tags_by_month(folder_path, tags):
    overall_counts = defaultdict(int)
    file_tag_breakdown = []
    monthly_totals = defaultdict(int)
    monthly_tag_usage = defaultdict(lambda: defaultdict(int))

    timestamp_pattern = re.compile(r'data-timestamp="(\d{4})-(\d{2})-\d{2}T\d{2}:\d{2}:\d{2}Z"')

    for filename in os.listdir(folder_path):
        if not filename.lower().endswith('.html'):
            continue

        try:
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                content = f.read()

            # Split into chunks starting with each timestamp
            chunks = re.split(r'(data-timestamp="\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")', content)

            # Reconstruct tagged chunks and count
            for i in range(1, len(chunks), 2):
                timestamp_attr = chunks[i]
                html_chunk = chunks[i] + chunks[i + 1] if i + 1 < len(chunks) else chunks[i]

                timestamp_match = timestamp_pattern.search(timestamp_attr)
                if not timestamp_match:
                    continue

                year, month = timestamp_match.groups()
                month_key = f"{year}-{month}"

                for tag in tags:
                    count = html_chunk.count(tag)
                    if count > 0:
                        overall_counts[tag] += count
                        file_tag_breakdown.append((filename, tag, count))
                        monthly_totals[month_key] += count
                        monthly_tag_usage[month_key][tag] += count

        except Exception as e:
            print(f"Error reading {filename}: {e}")

    # Final filter of zero-counts
    overall_counts = {tag: count for tag, count in overall_counts.items() if count > 0}
    return overall_counts, file_tag_breakdown, dict(monthly_totals), monthly_tag_usage

# CSV writers
def write_csv_overall(counts, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['tag', 'total_usage_count'])
        for tag, count in counts.items():
            writer.writerow([tag, count])
    print(f"Saved: {filename}")

def write_csv_file_breakdown(breakdown, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['filename', 'tag', 'usage_count'])
        for row in breakdown:
            writer.writerow(row)
    print(f"Saved: {filename}")

def write_csv_monthly_totals(month_totals, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['month', 'total_tag_usage'])
        for month in sorted(month_totals):
            writer.writerow([month, month_totals[month]])
    print(f"Saved: {filename}")

def write_csv_monthly_tag_usage(monthly_tag_usage, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['month', 'tag', 'usage_count'])
        for month in sorted(monthly_tag_usage):
            for tag in sorted(monthly_tag_usage[month]):
                writer.writerow([month, tag, monthly_tag_usage[month][tag]])
    print(f"Saved: {filename}")

# Main
if __name__ == '__main__':
    tags = load_tags('tags.ini')
    html_dir = 'analyst_folder'

    if tags:
        overall, breakdown, monthly_totals, monthly_tag_usage = count_tags_by_month(html_dir, tags)

        write_csv_overall(overall, 'report_overall_popularity.csv')
        write_csv_file_breakdown(breakdown, 'report_analyst_engagement.csv')
        write_csv_monthly_totals(monthly_totals, 'report_monthly_trend.csv')

