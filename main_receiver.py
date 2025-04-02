#!/usr/bin/env python3
import time
import csv
import sys
from rangepi_comm import open_rangepi_serial, configure_rangepi, read_rangepi_line

CSV_STORAGE_FILE = 'received_audio_data.csv'
SERIAL_PORT = '/dev/ttyACM0'
BAUDRATE = 9600

def process_csv_row(row):
    """
    Process a CSV row. Here we simply print an alert if the frequency is below a threshold.
    """
    try:
        timestamp, frequency, amplitude = row
        if float(frequency) < 50:
            print(f"Alert: Frequency {frequency} Hz below threshold at {timestamp}")
    except Exception as e:
        print("Error processing row:", e)

def is_valid_csv_line(line):
    """
    Check if a line is a valid CSV row by counting commas.
    We expect at least two commas (i.e. three fields).
    """
    return line.count(',') >= 2

def main():
    print("Starting Receiver on Raspberry Pi Zero W...", flush=True)
    ser = open_rangepi_serial(SERIAL_PORT, BAUDRATE)
    if not ser:
        print("Failed to open serial port. Exiting.", flush=True)
        sys.exit(1)

    # Configure dongle for RX mode
    print("Configuring dongle to RX mode...", flush=True)
    configure_rangepi(ser, mode="RX")
    time.sleep(0.5)

    # Flush any leftover data from configuration
    if ser.in_waiting:
        flushed = ser.read(ser.in_waiting)
        print("Flushed leftover data:", flushed, flush=True)
    
    print("Receiver: Listening for data...", flush=True)

    try:
        while True:
            # Debug: Check for any raw data in the buffer
            if ser.in_waiting:
                raw = ser.read(ser.in_waiting)
                print("Raw data chunk:", raw, flush=True)
            # Read a full line (with a short timeout)
            line = read_rangepi_line(ser)
            if line:
                print("Received line:", line, flush=True)
                if is_valid_csv_line(line):
                    try:
                        row = next(csv.reader([line]))
                        # Append the row to the CSV file
                        with open(CSV_STORAGE_FILE, 'a', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(row)
                        process_csv_row(row)
                    except Exception as e:
                        print("Error processing CSV row:", e, flush=True)
                else:
                    print("Ignored non-CSV data:", line, flush=True)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Receiver stopping...", flush=True)
    except Exception as e:
        print("Exception in receiver loop:", e, flush=True)
    finally:
        ser.close()
        print("Serial port closed.", flush=True)

if __name__ == '__main__':
    main()
