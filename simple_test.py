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
    send_rangepi_data(ser, test_message)
    
    # If you have loopback wiring or an echo, try to read a response
    time.sleep(1)
    response = read_rangepi_line(ser)
    print("Response:", response)
    ser.close()

if __name__ == '__main__':
    main()
