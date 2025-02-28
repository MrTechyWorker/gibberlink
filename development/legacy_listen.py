#################################################################
#                                                               #
#         Under development....Precise and accurate sounds      #
#                                                               #
#################################################################

import numpy as np
import sounddevice as sd
import scipy.signal as signal

# Define parameters
SAMPLE_RATE = 44100  # 44.1 kHz
DURATION = 0.01  # Duration of each tone in seconds
FREQ_MAP = {  # 4-bit to frequency mapping
    '0000': 500, '0001': 1000, '0010': 1500, '0011': 2000,
    '0100': 2500, '0101': 3000, '0110': 3500, '0111': 4000,
    '1000': 4500, '1001': 5000, '1010': 5500, '1011': 6000,
    '1100': 6500, '1101': 7000, '1110': 7500, '1111': 8000
}
REVERSE_FREQ_MAP = {v: k for k, v in FREQ_MAP.items()}  # Reverse mapping
DEBUG_MODE = True  # Set to True to print raw frequencies detected
FREQ_TOLERANCE = 50  # Allow small variations in detected frequency

def find_closest_freq(detected_freq):
    for known_freq in REVERSE_FREQ_MAP:
        if abs(detected_freq - known_freq) <= FREQ_TOLERANCE:
            return known_freq
    return None

def detect_frequency(audio_signal, sample_rate):
    f, t, Zxx = signal.stft(audio_signal, fs=sample_rate, nperseg=441)
    power = np.abs(Zxx).mean(axis=1)
    detected_freq = f[np.argmax(power)]
    return round(detected_freq)

def listen_and_decode():
    print("Listening for Gibberlink signals... Press Ctrl+C to stop.")
    while True:
        decoded_bits = ""
        decoded_message = ""
        print("Waiting for a new transmission...")
        
        while True:
            recording = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
            sd.wait()
            
            recorded_signal = recording.flatten()
            detected_freq = detect_frequency(recorded_signal, SAMPLE_RATE)
            
            if DEBUG_MODE:
                print(f"Detected Frequency: {detected_freq} Hz")
            
            if '*' in decoded_message:
                if decoded_message:
                    print(f"Full Decoded Message: {decoded_message}")
                break  # End of transmission, wait for new message
            
            matched_freq = find_closest_freq(detected_freq)
            
            if matched_freq:
                bit_chunk = REVERSE_FREQ_MAP[matched_freq]
                decoded_bits += bit_chunk
                
                while len(decoded_bits) >= 8:
                    byte = decoded_bits[:8]
                    decoded_bits = decoded_bits[8:]
                    decoded_char = chr(int(byte, 2))
                    decoded_message += decoded_char
                    print(f"Decoded Character: {decoded_char}")

if __name__ == "__main__":
    listen_and_decode()
