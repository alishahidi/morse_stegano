"""
Morse code utilities for audio steganography.
This module provides functions for converting between text and Morse code.
"""

from typing import Dict

# Morse code dictionary mapping characters to their Morse code representation
MORSE_CODE_DICT: Dict[str, str] = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ',': '--..--', '.': '.-.-.-', '?': '..--..',
    '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-', ' ': '/'
}

# Reverse mapping from Morse code to characters
REVERSE_MORSE_CODE_DICT: Dict[str, str] = {v: k for k, v in MORSE_CODE_DICT.items()}

def text_to_morse(text: str) -> str:
    """
    Convert text to Morse code.
    
    Args:
        text (str): Input text to convert
        
    Returns:
        str: Morse code representation of the input text
        
    Example:
        >>> text_to_morse("HELLO")
        '.... . .-.. .-.. ---'
    """
    return ' '.join(MORSE_CODE_DICT.get(char.upper(), '') for char in text)

def morse_to_text(morse: str) -> str:
    """
    Convert Morse code to text.
    
    Args:
        morse (str): Morse code string to convert
        
    Returns:
        str: Text representation of the Morse code
        
    Example:
        >>> morse_to_text('.... . .-.. .-.. ---')
        'HELLO'
    """
    return ''.join(REVERSE_MORSE_CODE_DICT.get(code, '') for code in morse.split())
