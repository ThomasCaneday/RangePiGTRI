import time
import board
import busio
from digitalio import DigitalInOut, Direction
import adafruit_rfm9x

# --- Configure RangePi mode pins if required ---
# Update these pins to the ones used on your board.
mode0 = DigitalInOut(board.GP7)
mode1 = DigitalInOut(board.GP8)
mode0.direction = Direction.OUTPUT
mode1.direction = Direction.OUTPUT
# Example mode setting; adjust according to your RangePi documentation.
mode0.value = True
mode1.value = False
# --- End mode configuration ---

# Set CS and RESET pins for the RFM9x module.
CS = DigitalInOut(board.GP5)    # update if needed
RESET = DigitalInOut(board.GP6) # update if needed

# Initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize the RFM9x radio at 915 MHz.
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)

print("LoRa Receiver running...")
while True:
    packet = rfm9x.receive()
    if packet is not None:
        # Decode the received bytes into a UTF-8 string.
        packet_text = str(packet, "utf-8")
        print("Received:", packet_text)
    time.sleep(0.1)
