# Audio Steganography with Morse Code

A Python-based command-line tool for hiding text messages within WAV audio files using Morse code encoding and LSB (Least Significant Bit) steganography.

## Features

- Encode text messages into WAV audio files using Morse code
- Decode hidden messages from steganographic WAV files
- Simple and intuitive command-line interface
- Robust error handling and validation
- Support for standard WAV audio files

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/audio_steganography.git
cd audio_steganography
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Encoding a Message

To hide a message in an audio file:

```bash
python cli.py encode input.wav "Your secret message" output.wav
```

### Decoding a Message

To extract a hidden message from an audio file:

```bash
python cli.py decode stego.wav
```

## How It Works

### Technical Overview

The project uses a combination of Morse code encoding and LSB (Least Significant Bit) steganography to hide messages in audio files. Here's the detailed process:

1. **Text to Morse Code Conversion**
   - Input text is converted to Morse code using a predefined mapping
   - Each character is represented by a sequence of dots (.) and dashes (-)
   - Words are separated by spaces, and letters within words are separated by slashes (/)

2. **Morse Code to Bitstream**
   - Morse code is converted to a binary bitstream
   - Dots (.) are represented as '1'
   - Dashes (-) are represented as '111'
   - Spaces between letters are represented as '000'
   - Spaces between words are represented as '0000000'
   - An end marker (20 zeros) is added to mark the end of the message

3. **LSB Steganography**
   - The audio file is read as a sequence of 16-bit samples
   - The least significant bit of each sample is replaced with a bit from the message
   - This modification is imperceptible to human ears
   - The modified samples are written back to a new WAV file

4. **Message Extraction**
   - The stego file is read sample by sample
   - The least significant bit of each sample is extracted
   - The bitstream is converted back to Morse code
   - Morse code is converted back to text

### Best Practices

1. **Audio File Selection**
   - Use WAV files with 16-bit depth
   - Choose files with sufficient length to accommodate your message
   - Avoid using compressed audio formats (MP3, OGG, etc.)
   - The audio file should be longer than your message

2. **Message Considerations**
   - Keep messages concise to ensure they fit in the audio file
   - Use only supported characters (A-Z, 0-9, and basic punctuation)
   - Avoid special characters that might not have Morse code equivalents
   - Consider the maximum message length based on the audio file size

3. **Security Considerations**
   - The hidden message is not encrypted, only concealed
   - Anyone with access to the stego file can extract the message
   - Consider encrypting the message before hiding it for additional security
   - Keep the original audio file secure to prevent comparison attacks

4. **Performance Tips**
   - Use shorter audio files for faster processing
   - Avoid very large audio files unless necessary
   - Keep messages as short as possible
   - Use simple audio files without complex waveforms

## Project Structure

```
audio_steganography/
├── cli.py           # Command-line interface
├── steg_core.py     # Core steganography functions
├── morse_utils.py   # Morse code utilities
└── requirements.txt # Project dependencies
```

## Requirements

- Python 3.7+
- numpy
- wave (built-in)
- click
- rich

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Example

Here's a complete example of how to use the tool:

1. First, prepare a WAV file to hide your message in:
```bash
# You can use any WAV file, or convert an MP3 to WAV using tools like ffmpeg
ffmpeg -i input.mp3 input.wav
```

2. Hide a message in the audio file:
```bash
python cli.py encode input.wav "This is a secret message" output.wav
```

3. Extract the hidden message:
```bash
python cli.py decode output.wav
```

The output should show: "This is a secret message" 