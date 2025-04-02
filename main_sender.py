# main_sender.py
from datetime import datetime
import time
from audio_recorder import AudioRecorder
from audio_processor import process_audio
from csv_handler import create_csv_row, write_csv_row
from rangepi_comm import open_rangepi_serial, configure_rangepi, send_rangepi_data

# --- Configuration ---
SERIAL_PORT = '/dev/ttyACM0'
BAUDRATE = 9600
CSV_FILE = 'audio_data.csv'
RECORD_SECONDS = 1
SAMPLE_RATE = 44100

def main():
    # Open serial connection for RangePi dongle
    ser = open_rangepi_serial(SERIAL_PORT, BAUDRATE)
    if ser is None:
        return

    # Configure dongle for transmission (TX mode)
    configure_rangepi(ser, mode="TX")

    # Initialize audio recording
    recorder = AudioRecorder(rate=SAMPLE_RATE, record_seconds=RECORD_SECONDS)
    print("Starting audio recording and transmission. Press Ctrl+C to stop.")
    
    try:
        while True:
            # Create a timestamp and record/process audio
            timestamp = datetime.now().isoformat()
            audio_data = recorder.record_audio()
            dominant_freq, amplitude = process_audio(audio_data, SAMPLE_RATE)
            
            # Create CSV row and write locally
            row = create_csv_row(timestamp, dominant_freq, amplitude)
            write_csv_row(CSV_FILE, row)
            
            # Prepare CSV-formatted string for transmission
            csv_data = f"{timestamp},{dominant_freq},{amplitude}\n"
            latency, bytes_sent = send_rangepi_data(ser, csv_data)
            if latency is not None:
                data_rate = bytes_sent / latency
                print(f"Sent {bytes_sent} bytes in {latency:.4f}s ({data_rate:.2f} B/s)")
            else:
                print("Failed to send data.")
            time.sleep(0.1)  # Adjust loop timing as needed
    except KeyboardInterrupt:
        print("Stopping transmitter.")
    finally:
        recorder.terminate()
        ser.close()

if __name__ == '__main__':
    main()
