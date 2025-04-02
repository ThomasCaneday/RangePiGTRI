# main_sender.py
from datetime import datetime
import time
from audio_recorder import AudioRecorder
from audio_processor import process_audio
from csv_handler import create_csv_row, write_csv_row
from rangepi_comm import open_rangepi_serial, configure_rangepi, send_rangepi_data

# --- Configuration ---
SERIAL_PORT = '/dev/ttyUSB0'  # Update if necessary
BAUDRATE = 9600
CSV_FILE = 'audio_data.csv'
RECORD_SECONDS = 1
SAMPLE_RATE = 44100

def main():
    # Open and configure the RangePi dongle
    ser = open_rangepi_serial(SERIAL_PORT, BAUDRATE)
    if ser is None:
        return
    configure_rangepi(ser)
    
    # Initialize audio recording
    recorder = AudioRecorder(rate=SAMPLE_RATE, record_seconds=RECORD_SECONDS)
    print("Starting audio recording and transmission. Press Ctrl+C to stop.")
    
    try:
        while True:
            # Create a timestamp
            timestamp = datetime.now().isoformat()
            # Record audio for the specified duration
            audio_data = recorder.record_audio()
            # Process audio data (extract dominant frequency and amplitude)
            dominant_freq, amplitude = process_audio(audio_data, SAMPLE_RATE)
            # Create and write CSV row locally
            row = create_csv_row(timestamp, dominant_freq, amplitude)
            write_csv_row(CSV_FILE, row)
            # Format CSV row for transmission
            csv_row_str = f"{timestamp},{dominant_freq},{amplitude}\n"
            # Transmit data over the RangePi dongle
            latency, bytes_sent = send_rangepi_data(ser, csv_row_str)
            if latency is not None:
                data_rate = bytes_sent / latency  # bytes per second
                print(f"Sent {bytes_sent} bytes in {latency:.4f}s ({data_rate:.2f} B/s)")
            else:
                print("Transmission failed.")
            time.sleep(0.1)  # Adjust loop timing as needed
    except KeyboardInterrupt:
        print("Stopping recording and transmission...")
    finally:
        recorder.terminate()
        ser.close()

if __name__ == '__main__':
    main()
