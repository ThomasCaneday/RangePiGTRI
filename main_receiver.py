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
    Process the received CSV row (e.g., alert if frequency is below threshold).
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

    # Configure dongle for reception (RX mode)
    configure_rangepi(ser, mode="RX")

    print("Receiver: Listening for data...")
    try:
        while True:
            line = read_rangepi_line(ser)
            if line:
                print("Received:", line)
                try:
                    row = next(csv.reader([line]))
                    write_csv_row(CSV_STORAGE_FILE, row)
                    process_csv_row(row)
                except Exception as e:
                    print("Error processing received data:", e)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping receiver.")
    finally:
        ser.close()

if __name__ == '__main__':
    main()
