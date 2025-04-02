# test_receiver.py
import serial
import time

def main():
    port = '/dev/ttyACM0'
    baudrate = 9600
    ser = serial.Serial(port, baudrate, timeout=1)
    time.sleep(2)  # Allow dongle to initialize
    print("Receiver: Listening for data...")

    try:
        while True:
            data = ser.readline().decode('utf-8').strip()
            if data:
                print("Received:", data)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Receiver stopping.")
    finally:
        ser.close()

if __name__ == '__main__':
    main()
