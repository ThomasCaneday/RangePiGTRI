# transmitter.py
import config
import utime
import st7789
import vga1_16x32 as font  # using one of the provided fonts

def send_message():
    # (Optional) Initialize display if you want visual feedback
    config.init_display("TRANSMITTER")
    
    print("Transmitter running. Type your message and press Enter to send.")
    while True:
        # Get message from terminal
        msg = input("Enter the message: ")
        if msg:
            # Append newline (if needed by your protocol)
            full_msg = msg + "\n"
            config.lora.write(full_msg)
            print("Sent:", msg)
            # (Optional) Update display if desired
            config.tft.text(font, "Sent: " + msg, 10, 60, st7789.YELLOW)
            utime.sleep(0.2)
            # Optionally clear or update display here

if __name__ == '__main__':
    send_message()
