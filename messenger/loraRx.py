#!/usr/bin/env python3
import time
import board
import busio
from digitalio import DigitalInOut
import adafruit_rfm9x

# Configure chip select (CS) and reset pins.
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)

# Initialize SPI bus using the Raspberry Pi's SPI pins.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize the RFM9x module on 915 MHz.
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)

print("LoRa Receiver running...")
while True:
    packet = rfm9x.receive()
    if packet is not None:
        try:
            packet_text = packet.decode("utf-8")
        except UnicodeDecodeError:
            packet_text = str(packet)
        print("Received:", packet_text)
    time.sleep(0.1)
