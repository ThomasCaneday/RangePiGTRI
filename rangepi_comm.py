# rangepi_comm.py
import serial
import time

def open_rangepi_serial(port='/dev/ttyACM0', baudrate=9600, timeout=1):
    """
    Open and return a serial connection to the RangePi dongle.
    """
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        time.sleep(2)  # Wait for dongle initialization
        return ser
    except Exception as e:
        print("Error opening serial port:", e)
        return None

def configure_rangepi(ser, mode="TX"):
    """
    Configure the RangePi dongle using AT commands.
    Use mode="TX" for transmitter or mode="RX" for receiver.
    Adjust these commands as required by your dongle's documentation.
    """
    if ser is None:
        print("Serial connection not available.")
        return

    # Set frequency to 915MHz
    freq_cmd = "AT+FREQ=915000000\r\n"
    ser.write(freq_cmd.encode('utf-8'))
    time.sleep(0.1)
    response = ser.readline().decode('utf-8').strip()
    print(f"Frequency config response: {response}")

    # Set device mode: TX or RX
    mode_cmd = f"AT+MODE={mode}\r\n"
    ser.write(mode_cmd.encode('utf-8'))
    time.sleep(0.1)
    response = ser.readline().decode('utf-8').strip()
    print(f"Mode config response: {response}")

def send_rangepi_data(ser, data):
    """
    Send data over the RangePi dongle.
    Returns latency (seconds) and number of bytes sent.
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
