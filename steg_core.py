import wave
import numpy as np
import logging
from typing import Tuple, Optional, Callable
from morse_utils import text_to_morse, morse_to_text

# Configure logging
log = logging.getLogger("audio_steganography")

class SteganographyError(Exception):
    """Base exception for steganography-related errors."""
    pass

class MessageTooLongError(SteganographyError):
    """Raised when the message is too long to embed in the audio file."""
    pass

class InvalidAudioFileError(SteganographyError):
    """Raised when the audio file is invalid or unsupported."""
    pass

class MessageNotFoundError(SteganographyError):
    """Raised when no message is found in the stego file."""
    pass

END_MARKER_BITS = '00000000000000000000'

def morse_to_bitstream(morse: str) -> str:
    """
    Convert Morse code to a binary bitstream.
    
    Args:
        morse (str): Morse code string
        
    Returns:
        str: Binary bitstream representation
    """
    log.debug("Converting Morse code to bitstream")
    morse += '|'  # end of message
    bitstream = ''
    for word in morse.split('/'):
        for char in word.split(' '):
            for symbol in char:
                bitstream += '1' * (3 if symbol == '-' else 1)
                bitstream += '0'
            bitstream = bitstream[:-1] + '000'
        bitstream = bitstream[:-3] + '0000000'
    return bitstream.rstrip('0') + END_MARKER_BITS

def bitstream_to_morse(bits: str) -> str:
    """
    Convert binary bitstream back to Morse code.
    
    Args:
        bits (str): Binary bitstream
        
    Returns:
        str: Morse code string
        
    Raises:
        MessageNotFoundError: If end marker is not found in the bitstream
    """
    log.debug("Converting bitstream to Morse code")
    if END_MARKER_BITS not in bits:
        raise MessageNotFoundError("No message found in the audio file")
    
    bits = bits[:bits.index(END_MARKER_BITS)]
    runs, prev, count = [], bits[0], 1
    
    for b in bits[1:]:
        if b == prev:
            count += 1
        else:
            runs.append((prev, count))
            prev = b
            count = 1
    runs.append((prev, count))

    morse = ''
    for bit, length in runs:
        if bit == '1':
            morse += '-' if length >= 3 else '.'
        else:
            if length >= 7:
                morse += ' / '
            elif length >= 3:
                morse += ' '
    return morse.strip()

def read_wav_file(file_path: str) -> Tuple[np.ndarray, wave.Wave_read]:
    """
    Read a WAV file and return its samples and parameters.
    
    Args:
        file_path (str): Path to the WAV file
        
    Returns:
        Tuple[np.ndarray, wave.Wave_read]: Audio samples and WAV parameters
        
    Raises:
        InvalidAudioFileError: If the file is not a valid WAV file
    """
    log.debug(f"Reading WAV file: {file_path}")
    try:
        with wave.open(file_path, 'rb') as wav:
            params = wav.getparams()
            frames = wav.readframes(params.nframes)
            samples = np.frombuffer(frames, dtype=np.int16)
            log.debug(f"Successfully read {len(samples)} samples")
            return samples, params
    except Exception as e:
        raise InvalidAudioFileError(f"Failed to read WAV file: {str(e)}")

def embed_message(input_wav: str, message: str, output_wav: str, progress_callback: Optional[Callable[[int], None]] = None) -> None:
    """
    Embed a message into a WAV file using LSB steganography.
    
    Args:
        input_wav (str): Path to input WAV file
        message (str): Message to embed
        output_wav (str): Path to output stego WAV file
        progress_callback (Optional[Callable[[int], None]]): Callback function for progress updates
        
    Raises:
        MessageTooLongError: If the message is too long to embed
        InvalidAudioFileError: If the audio file is invalid
    """
    log.info("Starting message embedding process")
    
    # Convert message to Morse code and bitstream
    morse = text_to_morse(message)
    bitstream = morse_to_bitstream(morse)
    log.debug(f"Message converted to {len(bitstream)} bits")
    
    # Read input file
    try:
        samples, params = read_wav_file(input_wav)
    except Exception as e:
        raise InvalidAudioFileError(f"Failed to read input WAV file: {str(e)}")

    # Check if message fits
    if len(bitstream) > len(samples):
        raise MessageTooLongError(
            f"Message too long to embed. Maximum length: {len(samples)} bits"
        )

    # Embed the message
    log.debug("Embedding message into audio samples")
    samples_mod = samples.copy()
    total_bits = len(bitstream)
    
    for i, bit in enumerate(bitstream):
        samples_mod[i] = (samples_mod[i] & ~1) | int(bit)
        if progress_callback and i % (total_bits // 100) == 0:
            progress_callback(int((i / total_bits) * 100))

    # Write output file
    log.debug(f"Writing output file: {output_wav}")
    try:
        with wave.open(output_wav, 'wb') as wav:
            wav.setparams(params)
            wav.writeframes(samples_mod.tobytes())
    except Exception as e:
        raise InvalidAudioFileError(f"Failed to write output WAV file: {str(e)}")
    
    log.info("Message embedding completed successfully")

def extract_message(stego_wav: str, progress_callback: Optional[Callable[[int], None]] = None) -> str:
    """
    Extract a hidden message from a stego WAV file.
    
    Args:
        stego_wav (str): Path to stego WAV file
        progress_callback (Optional[Callable[[int], None]]): Callback function for progress updates
        
    Returns:
        str: Extracted message
        
    Raises:
        MessageNotFoundError: If no message is found in the file
        InvalidAudioFileError: If the audio file is invalid
    """
    log.info("Starting message extraction process")
    
    # Read stego file
    try:
        samples, _ = read_wav_file(stego_wav)
    except Exception as e:
        raise InvalidAudioFileError(f"Failed to read stego WAV file: {str(e)}")

    # Extract bits
    log.debug("Extracting bits from audio samples")
    total_samples = len(samples)
    bits = []
    
    for i, sample in enumerate(samples):
        bits.append(str(sample & 1))
        if progress_callback and i % (total_samples // 100) == 0:
            progress_callback(int((i / total_samples) * 100))
    
    bitstream = ''.join(bits)
    
    # Convert to text
    try:
        morse = bitstream_to_morse(bitstream)
        message = morse_to_text(morse)
        log.info("Message extraction completed successfully")
        return message
    except MessageNotFoundError:
        raise MessageNotFoundError("No hidden message found in the audio file")
