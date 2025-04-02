# csv_handler.py

import csv
import os

def create_csv_row(timestamp, frequency, amplitude):
    """
    Create a CSV row list.
    """
    return [timestamp, frequency, amplitude]

def write_csv_row(file_path, row):
    """
    Append a CSV row to the given file. Creates the file with a header if it doesn't exist.
    """
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['timestamp', 'frequency', 'amplitude'])
        writer.writerow(row)
