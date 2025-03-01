import numpy as np
import sounddevice as sd
import scipy.signal as signal
from loguru import logger
import string


class Listener:
    def __init__(self, debug_mode : bool = True, message_end_char : str = "*"):
        self.SAMPLE_RATE = 44100
        self.DURATION = 0.09
        self.FREQ_MAP : dict = {
            '0000': 500, '0001': 1000, '0010': 1500, '0011': 2000,
            '0100': 2500, '0101': 3000, '0110': 3500, '0111': 4000,
            '1000': 4500, '1001': 5000, '1010': 5500, '1011': 6000,
            '1100': 6500, '1101': 7000, '1110': 7500, '1111': 8000
        }
        self.DEBUG_MODE = debug_mode
        self.CHUNK_SIZE = 4
        self.MESSAGE_END_CHAR = message_end_char

        self.N_SAMPLES = int(self.SAMPLE_RATE * self.DURATION)
        self.INV_FREQ_MAP = {v: k for k, v in self.FREQ_MAP.items()}

    def _is_valid_char(self, char):
        return char in string.printable and char not in string.whitespace

    def listen(self) -> str:
        binary_string = ""
        decoded_message = ""
        stop_event = [False]  # Use a mutable list to allow modification inside the callback

        def callback(indata, frames, time, status):
            nonlocal binary_string, decoded_message

            if status:
                logger.warning(status)

            # Perform FFT to detect dominant frequency
            freqs, psd = signal.welch(indata[:, 0], self.SAMPLE_RATE, nperseg=self.N_SAMPLES)
            detected_freq = freqs[np.argmax(psd)]

            # Find the closest known frequency
            closest_freq = min(self.INV_FREQ_MAP.keys(), key=lambda x: abs(x - detected_freq))
            binary_chunk = self.INV_FREQ_MAP[closest_freq]

            logger.debug(f"Detected: {detected_freq} Hz -> Closest: {closest_freq} Hz -> Binary: {binary_chunk}") if self.DEBUG_MODE else ...

            binary_string += binary_chunk

            # Decode when we have full bytes
            while len(binary_string) >= 8:
                char_bin = binary_string[:8]
                binary_string = binary_string[8:]
                decoded_char: str = chr(int(char_bin, 2))
                if self._is_valid_char(decoded_char):
                    decoded_message += decoded_char
                logger.info(f"Decoded: '{decoded_char}'") if decoded_char != '\x00' else ...

                if decoded_char == self.MESSAGE_END_CHAR:
                    logger.success(f"Full Message: {decoded_message}")
                    stop_event[0] = True  # Signal to stop listening
                    return

        with sd.InputStream(callback=callback, channels=1, samplerate=self.SAMPLE_RATE, blocksize=self.N_SAMPLES):
            logger.info("Listening for Gibberlink signals...")
            while not stop_event[0]:
                sd.sleep(100)  # Reduce CPU usage while waiting

        return decoded_message  # Return the full decoded message
