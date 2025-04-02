# transmitter_test.py
from rangepi_comm import open_rangepi_serial, send_rangepi_data
import time

ser = open_rangepi_serial()
if ser:
    while True:
        latency, bytes_sent = send_rangepi_data(ser, "Test\n")
        print(f"Sent {bytes_sent} bytes, latency: {latency:.4f}s")
        time.sleep(1)
    ser.close()
else:
    print("Serial port not available.")
