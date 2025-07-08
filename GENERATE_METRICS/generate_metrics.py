import os
import csv

# This function handles reading and opening of each file and counting occurrences.
def count_string_in_file(file_path, target_string):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content.count(target_string)
    except FileNotFoundError:
        print(f"❌ File not found: '{file_path}'. Skipping this file.")
    except Exception as e:
        print(f"⚠️ An error occurred while reading '{file_path}': {e}")
    return None  # Return None to indicate an error

# This function counts the overall amount of occurrences of the string.
def count_string_in_folder(folder_path, target_string):
    total_count = 0
    file_counts = {}

    try:
        filenames = os.listdir(folder_path)
    except FileNotFoundError:
        print(f"❌ Folder not found: '{folder_path}'. Please check the folder path and try again.")
        return {}, 0
    except Exception as e:
        print(f"⚠️ An error occurred accessing the folder '{folder_path}': {e}")
        return {}, 0

    for filename in filenames:
        if filename.endswith('.html'):
            file_path = os.path.join(folder_path, filename)
            count = count_string_in_file(file_path, target_string)
            if count is not None:  # Only include if file was successfully read
                file_counts[filename] = count
                total_count += count

    return file_counts, total_count

# Folder to search and string to find
folder_path = 'analyst_folder'
string_to_count = '[grc-'

file_counts, total = count_string_in_folder(folder_path, string_to_count)

# Output to CSV
output_file = 'report_overall_popularity.csv'
try:
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Filename', 'Occurrences'])
        for file, count in file_counts.items():
            writer.writerow([file, count])
        writer.writerow(['TOTAL', total])
    print(f"✅ Results written to '{output_file}'")
except Exception as e:
    print(f"⚠️ Could not write to CSV file: {e}")
