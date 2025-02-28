#################################################################
#                                                               #
#         Under development....Precise and accurate sounds      #
#                                                               #
#################################################################

import numpy as np
import sounddevice as sd
import time
from loguru import logger

# Define parameters
SAMPLE_RATE = 44100  # 44.1 kHz
DURATION = 0.1  # Duration of each tone in seconds
FREQ_MAP = {  # 4-bit to frequency mapping
    '0000': 500, '0001': 1000, '0010': 1500, '0011': 2000,
    '0100': 2500, '0101': 3000, '0110': 3500, '0111': 4000,
    '1000': 4500, '1001': 5000, '1010': 5500, '1011': 6000,
    '1100': 6500, '1101': 7000, '1110': 7500, '1111': 8000
}
DEBUG_MODE = True  # Enable debugging output

# Function to generate a tone
def generate_tone(frequency, duration):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * frequency * t)

# Function to encode a message into Gibberlink signals
def encode_message(message):
    binary_string = ''.join(format(ord(c), '08b') for c in message)
    logger.info(f"Message: {message}")
    logger.info(f"Binary Representation: {binary_string}")
    logger.debug("Transmitting...")
    
    for i in range(0, len(binary_string), 4):
        chunk = binary_string[i:i+4]
        if len(chunk) < 4:
            chunk = chunk.ljust(4, '0')  # Pad if needed
        
        frequency = FREQ_MAP.get(chunk, 500)  # Default to 500 Hz if missing
        
        if DEBUG_MODE:
            logger.debug(f"Chunk: {chunk} -> Frequency: {frequency} Hz")
        
        tone = generate_tone(frequency, DURATION)
        sd.play(tone, samplerate=SAMPLE_RATE)
        sd.wait()
        time.sleep(0.01)  # Short delay between transmissions

if __name__ == "__main__":
    encode_message("HELLO*")
    logger.success("Done Transmitting!")