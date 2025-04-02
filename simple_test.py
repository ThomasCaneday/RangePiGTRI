# simple_test.py
from rangepi_comm import open_rangepi_serial, configure_rangepi, send_rangepi_data, read_rangepi_line
import time

def main():
    ser = open_rangepi_serial()
    if not ser:
        print("Serial port not available.")
        return
      
    print("Configuring dongle to TX mode...")
    configure_rangepi(ser, mode="TX")
    time.sleep(1)
      
    test_message = "Hello World\n"
    print("Sending test message...")
    latency, bytes_sent = send_rangepi_data(ser, test_message)
    if latency is not None:
        print(f"Sent {bytes_sent} bytes in {latency:.4f} seconds.")
    else:
        print("Failed to send test message.")
      
    # If you have a loopback or echo, attempt to read a response.
    time.sleep(1)
    response = read_rangepi_line(ser)
    if response:
        print("Response:", response)
    else:
        print("No response received.")
      
    ser.close()

if __name__ == '__main__':
    main()
