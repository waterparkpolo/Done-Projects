This Python script counts how many times a specific string
(such as a tag or word) appears in multiple .html files within a given folder.
Simply put the htmls in the folder and the program will count how many times
ai was accessed using the '[grc-' string, this can be changed to any string like
timestamp to catch all instances of that string in each html file.
The program then exports the data to a csv file named report_overall_popularity.csv.
Each row in the CSV will contain: filename, occurrence_count.

The last row will show the total count across all files.

If the file is not found or other errors occur, the program will exit with a user friendly error message


Requirements

Python 3.x

No external libraries required (uses only built-in modules)
import os
import csv

How to Use

Prepare Your Files
Place all your .html files in a folder.
Open count_strings.py and update the following lines:

folder_path = 'analyst_folder'   #This is the folder name
string_to_count = '[grc-'      # Replace with the string you want to search for


Run the Script
Open a terminal or command prompt and run:
python count_strings.py
The script will:
Loop through all .html files in the specified folder
Count how many times the given string appears in each file
Print a summary per file and a total

Count of '[grc-' in HTML files in folder 'analyst_folder':

Example:
  page1.html: 14 occurrences
  page2.html: 9 occurrences
  page3.html: 20 occurrences

Total across all files: 43

