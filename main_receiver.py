# main_receiver.py
import time
import csv
from csv_handler import write_csv_row
from rangepi_comm import open_rangepi_serial, read_rangepi_line

CSV_STORAGE_FILE = 'received_audio_data.csv'
SERIAL_PORT = '/dev/ttyUSB0'
BAUDRATE = 9600

def process_csv_row(row):
    """
    Process the received CSV row (example: alert if frequency < 50 Hz).
    """
    try:
        timestamp, frequency, amplitude = row
        if float(frequency) < 50:
            print(f"Alert: Frequency {frequency} Hz below threshold at {timestamp}")
    except Exception as e:
        print("Error processing row:", e)

def main():
    ser = open_rangepi_serial(SERIAL_PORT, BAUDRATE)
    if ser is None:
        return

    print("Receiver running. Waiting for data...")
    while True:
        line = read_rangepi_line(ser)
        if line:
            print(f"Received: {line}")
            try:
                row = next(csv.reader([line]))
                write_csv_row(CSV_STORAGE_FILE, row)
                process_csv_row(row)
            except Exception as e:
                print("Error processing received data:", e)
        time.sleep(0.1)

if __name__ == '__main__':
    main()
