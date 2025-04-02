#!/usr/bin/env python3
import time
import board
import busio
from digitalio import DigitalInOut
import adafruit_rfm9x

# Configure chip select (CS) and reset pins.
# These are set according to the sample: adjust if your wiring is different.
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)

# Initialize SPI bus using the Raspberry Pi's SPI pins.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize the RFM9x module on 915 MHz.
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23  # Set transmit power (dBm)

# Data to be sent.
data = bytes("hey all medium viewers", "utf-8")

print("LoRa Transmitter running...")
while True:
    rfm9x.send(data)
    print("Data sent")
    time.sleep(2)
