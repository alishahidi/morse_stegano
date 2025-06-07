import wave
import numpy as np
from morse_utils import text_to_morse, morse_to_text

END_MARKER_BITS = '00000000000000000000'

def morse_to_bitstream(morse: str) -> str:
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
    if END_MARKER_BITS not in bits:
        raise ValueError("End marker not found")
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

def embed_message(input_wav, message, output_wav):
    morse = text_to_morse(message)
    bitstream = morse_to_bitstream(morse)

    with wave.open(input_wav, 'rb') as wav:
        params = wav.getparams()
        frames = wav.readframes(params.nframes)
    samples = np.frombuffer(frames, dtype=np.int16)

    if len(bitstream) > len(samples):
        raise ValueError("Message too long to embed")

    samples_mod = samples.copy()
    for i, bit in enumerate(bitstream):
        samples_mod[i] = (samples_mod[i] & ~1) | int(bit)

    with wave.open(output_wav, 'wb') as wav:
        wav.setparams(params)
        wav.writeframes(samples_mod.tobytes())

def extract_message(stego_wav):
    with wave.open(stego_wav, 'rb') as wav:
        frames = wav.readframes(wav.getnframes())
    samples = np.frombuffer(frames, dtype=np.int16)

    bits = ''.join(str(s & 1) for s in samples)
    morse = bitstream_to_morse(bits)
    return morse_to_text(morse)
