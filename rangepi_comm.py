# rangepi_comm.py
import serial
import time

def open_rangepi_serial(port='/dev/ttyACM0', baudrate=9600, timeout=0.5):
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

def read_line_with_timeout(ser, timeout=1.0):
    start_time = time.time()
    line = b""
    while time.time() - start_time < timeout:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            print("DEBUG: Read data chunk:", data)  # Debug output
            line += data
            if b'\n' in line:
                break
        else:
            print("DEBUG: No data waiting")
        time.sleep(0.05)
    return line.decode('utf-8').strip() if line else None

def configure_rangepi(ser, mode="TX"):
    """
    Configure the RangePi dongle using AT commands.
    Use mode="TX" for transmitter or mode="RX" for receiver.
    """
    if ser is None:
        print("Serial connection not available.")
        return

    # Set frequency to 915MHz
    freq_cmd = "AT+FREQ=915000000\r\n"
    ser.write(freq_cmd.encode('utf-8'))
    time.sleep(0.1)
    freq_response = read_line_with_timeout(ser, timeout=1.0)
    if freq_response:
        print(f"Frequency config response: {freq_response}")
    else:
        print("No frequency response received.")

    # Set device mode: TX or RX
    mode_cmd = f"AT+MODE={mode}\r\n"
    ser.write(mode_cmd.encode('utf-8'))
    time.sleep(0.1)
    mode_response = read_line_with_timeout(ser, timeout=1.0)
    if mode_response:
        print(f"Mode config response: {mode_response}")
    else:
        print("No mode response received.")

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
    Read a line from the RangePi dongle using our timeout function.
    """
    return read_line_with_timeout(ser, timeout=1.0)
