# receiver.py
import config
import utime
import st7789
import vga1_16x32 as font  # using one of the provided fonts

def receive_message():
    # (Optional) Initialize display if you want visual feedback
    config.init_display("RECEIVER")
    
    print("Receiver running. Waiting for messages...")
    while True:
        data = config.lora.readline()  # Read data from LoRa
        if data:
            # Convert bytes to string if necessary
            message = data.decode('utf-8').strip() if isinstance(data, bytes) else str(data)
            print("Received:", message)
            # (Optional) Display the message on the TFT
            config.tft.text(font, "Rx: " + message, 10, 60, st7789.YELLOW)
            utime.sleep(0.2)

if __name__ == '__main__':
    receive_message()
