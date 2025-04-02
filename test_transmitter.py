# test_transmitter.py
import serial
import time

def main():
    port = '/dev/ttyACM0'
    baudrate = 9600
    ser = serial.Serial(port, baudrate, timeout=1)
    time.sleep(2)  # Allow dongle to initialize

    test_message = "Hello from Transmitter!\n"
    print("Transmitter: Sending:", test_message.strip())
    ser.write(test_message.encode('utf-8'))
    ser.flush()

    ser.close()

if __name__ == '__main__':
    main()
