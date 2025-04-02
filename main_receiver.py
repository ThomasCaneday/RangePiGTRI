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
    Process the received CSV row. For example, if frequency is below a threshold, print an alert.
    """
    try:
        timestamp, frequency, amplitude = row
        if float(frequency) < 50:
            print(f"Alert: Frequency {frequency} Hz below threshold at {timestamp}")
    except Exception as e:
        print("Error processing row:", e)

def is_valid_csv_line(line):
    """
    Check if the line looks like a valid CSV row. We expect at least two commas.
    """
    return line.count(',') >= 2

def main():
    # Open serial port
    ser = open_rangepi_serial(SERIAL_PORT, BAUDRATE)
    if ser is None:
        print("Failed to open serial port.")
        return

    # Configure dongle for RX mode
    print("Configuring dongle to RX mode...")
    configure_rangepi(ser, mode="RX")
    
    # Optionally flush any leftover configuration data
    time.sleep(0.5)
    if ser.in_waiting:
        flushed = ser.read(ser.in_waiting)
        print("Flushed data after config:", flushed)
    
    print("Receiver: Listening for data...")

    try:
        while True:
            # Debug: Print any raw data available in the input buffer
            if ser.in_waiting:
                raw = ser.read(ser.in_waiting)
                print("Raw data chunk:", raw)
            
            # Read a line with our helper function
            line = read_rangepi_line(ser)
            if line:
                print("Received line:", line)
                if is_valid_csv_line(line):
                    try:
                        row = next(csv.reader([line]))
                        write_csv_row(CSV_STORAGE_FILE, row)
                        process_csv_row(row)
                    except Exception as e:
                        print("Error processing received CSV data:", e)
                else:
                    print("Ignored non-CSV data:", line)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Receiver stopping.")
    finally:
        ser.close()

if __name__ == '__main__':
    main()
