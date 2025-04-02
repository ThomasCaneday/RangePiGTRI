# rangepi_comm.py
import serial
import time

def open_rangepi_serial(port='/dev/ttyACM0', baudrate=9600, timeout=0.3):
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        time.sleep(2)  # Wait for dongle initialization
        return ser
    except Exception as e:
        print("Error opening serial port:", e)
        return None

def read_line_with_timeout(ser, timeout=0.3):
    start_time = time.time()
    line = b""
    while time.time() - start_time < timeout:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            line += data
            if b'\n' in line:
                break
        time.sleep(0.05)
    response = line.decode('utf-8').strip() if line else ""
    # Filter out typical REPL prompt and syntax error lines
    filtered_lines = []
    for l in response.splitlines():
        if l.strip() in (">>>", "") or l.strip().startswith("SyntaxError"):
            continue
        filtered_lines.append(l.strip())
    return "\n".join(filtered_lines)

def configure_rangepi(ser, mode="TX"):
    if ser is None:
        print("Serial connection not available.")
        return

    # Set frequency to 915MHz
    freq_cmd = "AT+FREQ=915000000\r\n"
    ser.write(freq_cmd.encode('utf-8'))
    time.sleep(0.1)
    freq_response = read_line_with_timeout(ser, timeout=0.3)
    if freq_response:
        print(f"Frequency config response: {freq_response}")
    else:
        print("No frequency response received. Assuming command accepted.")

    # Set device mode: TX or RX
    mode_cmd = f"AT+MODE={mode}\r\n"
    ser.write(mode_cmd.encode('utf-8'))
    time.sleep(0.1)
    mode_response = read_line_with_timeout(ser, timeout=0.3)
    if mode_response:
        print(f"Mode config response: {mode_response}")
    else:
        print("No mode response received. Assuming command accepted.")

def send_rangepi_data(ser, data):
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
    return read_line_with_timeout(ser, timeout=0.3)
