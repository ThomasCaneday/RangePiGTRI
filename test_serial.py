# test_serial.py
import serial
import time

def main():
    port = '/dev/ttyACM0'
    baudrate = 9600
    ser = serial.Serial(port, baudrate, timeout=1)
    time.sleep(2)  # Wait for dongle initialization

    # NOTE: For a loopback test, physically connect the TX and RX pins on the dongle.
    test_message = "Hello, RangePi Test!\n"
    print("Sending:", test_message.strip())
    ser.write(test_message.encode('utf-8'))
    ser.flush()

    # Wait briefly to allow the message to loop back
    time.sleep(1)

    response = ser.readline().decode('utf-8').strip()
    if response:
        print("Received:", response)
    else:
        print("No response received. Check your loopback connection or dongle configuration.")

    ser.close()

if __name__ == '__main__':
    main()
