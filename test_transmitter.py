# test_transmitter.py
from rangepi_comm import open_rangepi_serial, configure_rangepi, send_rangepi_data
import time

def main():
    ser = open_rangepi_serial()
    if ser is None:
        return

    # Configure dongle for transmission (TX mode)
    configure_rangepi(ser, mode="TX")
    time.sleep(1)  # Wait for settings to take effect

    test_message = "Hello from Transmitter!\n"
    print("Transmitter: Sending:", test_message.strip())
    latency, bytes_sent = send_rangepi_data(ser, test_message)
    if latency is not None:
        print(f"Sent {bytes_sent} bytes in {latency:.4f} seconds.")
    else:
        print("Failed to send data.")

    ser.close()

if __name__ == '__main__':
    main()
