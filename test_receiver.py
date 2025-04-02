# test_receiver.py
from rangepi_comm import open_rangepi_serial, configure_rangepi, read_rangepi_line
import time

def main():
    ser = open_rangepi_serial()
    if ser is None:
        return

    # Configure dongle for reception (RX mode)
    configure_rangepi(ser, mode="RX")
    time.sleep(1)  # Wait for settings to take effect

    print("Receiver: Listening for data...")
    try:
        while True:
            data = read_rangepi_line(ser)
            if data:
                print("Received:", data)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Receiver stopping.")
    finally:
        ser.close()

if __name__ == '__main__':
    main()
