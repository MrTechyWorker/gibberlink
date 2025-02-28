import numpy as np
import sounddevice as sd
from loguru import logger
import numpy as np

class Talker:
    def __init__(self, debug_mode : bool = True):
        self.DEBUG_MODE = debug_mode
        
        self.SAMPLE_RATE = 44100
        self.DURATION = 0.09
        self.FREQ_MAP = {
            '0000': 500, '0001': 1000, '0010': 1500, '0011': 2000,
            '0100': 2500, '0101': 3000, '0110': 3500, '0111': 4000,
            '1000': 4500, '1001': 5000, '1010': 5500, '1011': 6000,
            '1100': 6500, '1101': 7000, '1110': 7500, '1111': 8000
        }
        self.CHUNK_SIZE = 4
        self.MESSAGE_END_CHAR = '***'
        self.PRECOMPUTED_TONES = {freq: 0.5 * np.sin(2 * np.pi * freq * np.linspace(0, self.DURATION, int(self.SAMPLE_RATE * self.DURATION), endpoint=False)) for freq in self.FREQ_MAP.values()}

    def talk(self, message: str) -> None:
        message += self.MESSAGE_END_CHAR 
        binary_string = ''.join(format(ord(c), '08b') for c in message)
        logger.info(f"Message: {message}")
        logger.info(f"Binary Representation: {binary_string}")

        full_signal = np.array([])  # Store all tones in one array

        for i in range(0, len(binary_string), self.CHUNK_SIZE):

            chunk = binary_string[i:i+self.CHUNK_SIZE].ljust(self.CHUNK_SIZE, '0')
            frequency = self.FREQ_MAP.get(chunk, 500)

            if self.DEBUG_MODE:
                logger.debug(f"Chunk: {chunk} -> Frequency: {frequency} Hz")

            full_signal = np.concatenate((full_signal, self.PRECOMPUTED_TONES[frequency]))

        sd.play(full_signal, samplerate=self.SAMPLE_RATE)
        sd.wait()
        logger.success("Transmission Complete!")