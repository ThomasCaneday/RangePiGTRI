# main_receiver.py
import time
import csv
from csv_handler import write_csv_row
from rangepi_comm import open_rangepi_serial, configure_rangepi, read_rangepi_line

CSV_STORAGE_FILE = 'received_audio_data.csv'
SERIAL_PORT = '/dev/ttyACM0'
BAUDRATE = 9600

def process_csv_row(row):
    """
    Process the received CSV row (e.g., alert if frequency is below a threshold).
    """
    try:
        timestamp, frequency, amplitude = row
        if float(frequency) < 50:
            print(f"Alert: Frequency {frequency} Hz below threshold at {timestamp}")
    except Exception as e:
        print("Error processing row:", e)

def is_valid_csv_line(line):
    """
    Check if the line looks like a valid CSV row.
    We expect at least two commas (three fields).
    """
    return line.count(',') >= 2

def flush_serial_buffer(ser):
    """
    Read and discard any data currently in the serial buffer.
    """
    time.sleep(0.5)
    while ser.in_waiting:
        ser.readline()

def main():
    ser = open_rangepi_serial(SERIAL_PORT, BAUDRATE)
    if ser is None:
        return

    # Configure dongle for reception (RX mode)
    configure_rangepi(ser, mode="RX")
    
    # Flush out any configuration responses before starting the listener.
    flush_serial_buffer(ser)
    
    print("Receiver: Listening for data...")
    try:
        while True:
            line = read_rangepi_line(ser)
            if line:
                # Only process lines that look like CSV data.
                if is_valid_csv_line(line):
                    print("Received:", line)
                    try:
                        row = next(csv.reader([line]))
                        write_csv_row(CSV_STORAGE_FILE, row)
                        process_csv_row(row)
                    except Exception as e:
                        print("Error processing received data:", e)
                else:
                    # Ignore lines that are not CSV data (like configuration echoes).
                    print("Ignored non-CSV data:", line)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping receiver.")
    finally:
        ser.close()

if __name__ == '__main__':
    main()
