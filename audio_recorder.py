# audio_recorder.py

import pyaudio
import numpy as np

class AudioRecorder:
    def __init__(self, channels=1, rate=44100, chunk=1024, record_seconds=1):
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.record_seconds = record_seconds
        self.format = pyaudio.paInt16  # 16-bit resolution
        self.audio_interface = pyaudio.PyAudio()

    def record_audio(self):
        stream = self.audio_interface.open(format=self.format,
                                             channels=self.channels,
                                             rate=self.rate,
                                             input=True,
                                             frames_per_buffer=self.chunk)
        frames = []
        for _ in range(0, int(self.rate / self.chunk * self.record_seconds)):
            data = stream.read(self.chunk, exception_on_overflow=False)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        # Combine frames and convert to a NumPy array
        audio_data = b''.join(frames)
        audio_np = np.frombuffer(audio_data, dtype=np.int16)
        return audio_np

    def terminate(self):
        self.audio_interface.terminate()

if __name__ == '__main__':
    recorder = AudioRecorder()
    try:
        print("Recording for 1 second...")
        data = recorder.record_audio()
        print("Recording complete. Data shape:", data.shape)
    finally:
        recorder.terminate()
