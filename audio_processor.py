# audio_processor.py

import numpy as np

def process_audio(audio_data, rate):
    """
    Process audio data to extract the dominant frequency and amplitude.

    Parameters:
        audio_data (np.array): The recorded audio samples.
        rate (int): The sampling rate.

    Returns:
        dominant_freq (float): Dominant frequency in Hz.
        amplitude (float): RMS amplitude of the audio.
    """
    # Compute FFT and corresponding frequencies
    fft_result = np.fft.rfft(audio_data)
    fft_magnitude = np.abs(fft_result)
    freqs = np.fft.rfftfreq(len(audio_data), d=1/rate)
    
    # Skip the zero frequency component and find the peak
    if len(fft_magnitude) > 1:
        dominant_index = np.argmax(fft_magnitude[1:]) + 1
        dominant_freq = freqs[dominant_index]
    else:
        dominant_freq = 0.0

    # Calculate RMS amplitude
    amplitude = np.sqrt(np.mean(audio_data**2))
    
    return dominant_freq, amplitude

if __name__ == '__main__':
    # For demonstration: process a generated sine wave signal
    import numpy as np
    rate = 44100
    t = np.linspace(0, 1, rate, endpoint=False)
    freq_test = 440  # Example: A4 note
    audio_data = (0.5 * np.sin(2 * np.pi * freq_test * t) * 32767).astype(np.int16)
    dominant_freq, amplitude = process_audio(audio_data, rate)
    print("Dominant Frequency:", dominant_freq, "Hz")
    print("Amplitude:", amplitude)
