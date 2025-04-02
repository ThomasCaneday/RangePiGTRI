# config.py
from machine import Pin, UART, SPI
import st7789
import utime

# Setup SPI and TFT display (optional)
spi = SPI(1, baudrate=40000000, sck=Pin(10), mosi=Pin(11))
tft = st7789.ST7789(spi, 135, 240,
                    reset=Pin(12, Pin.OUT),
                    cs=Pin(9, Pin.OUT),
                    dc=Pin(8, Pin.OUT),
                    backlight=Pin(13, Pin.OUT),
                    rotation=1)

# Configure LoRa UART interface
lora = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Configure mode pins (if required)
Mode0 = Pin(2, Pin.OUT)
Mode1 = Pin(3, Pin.OUT)
# Set modes as needed (for transmitter, receiver, or configuration)
Mode0.value(0)
Mode1.value(0)

# (Optional) Initialization for the display can be added here.
def init_display(title="MESSENGER"):
    tft.init()
    utime.sleep(0.2)
    tft.fill(0)  # Clear display
    tft.text(title, 5, 10, st7789.WHITE)
