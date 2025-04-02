# rangepi_comm.py
import serial
import time

def open_rangepi_serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1):
    """
    Open and return a serial connection to the RangePi dongle.
    """
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        time.sleep(2)  # Allow dongle time to initialize
        return ser
    except Exception as e:
        print("Error opening serial port:", e)
        return None

def configure_rangepi(ser):
    """
    Configure the RangePi dongle using commands adapted from sbcshop's RangePi code.
    Replace these example commands with the ones your dongle requires.
    """
    if ser is None:
        print("Serial connection not available for configuration.")
        return

    # Example configuration commands:
    config_commands = [
        "AT+FREQ=915000000",   # Set frequency to 915MHz
        "AT+MODE=TX"           # Set transmitter mode (adjust if needed)
        # Add more commands here if necessary (e.g., power, bandwidth, etc.)
    ]

    for cmd in config_commands:
        full_cmd = cmd + "\r\n"
        try:
            ser.write(full_cmd.encode('utf-8'))
            time.sleep(0.1)  # Give time for the dongle to process the command
            response = ser.readline().decode('utf-8').strip()
            print(f"Config sent: {cmd} -> Received: {response}")
        except Exception as e:
            print(f"Error sending command '{cmd}':", e)

def send_rangepi_data(ser, data):
    """
    Send data over the RangePi dongle.
    Returns the latency (in seconds) and the number of bytes sent.
    """
    if ser is None:
        print("Serial connection not available for sending.")
        return None, 0

    start_time = time.time()
    try:
        data_bytes = data.encode('utf-8')
        ser.write(data_bytes)
        ser.flush()
        end_time = time.time()
        return end_time - start_time, len(data_bytes)
    except Exception as e:
        print("Error sending data:", e)
        return None, 0

def read_rangepi_line(ser):
    """
    Read a line from the RangePi dongle.
    """
    if ser is None:
        return None
    try:
        return ser.readline().decode('utf-8').strip()
    except Exception as e:
        print("Error reading data:", e)
        return None
