import argparse
from steg_core import embed_message, extract_message  # renamed import


def main():
    parser = argparse.ArgumentParser(description='🔊 Morse Code Audio Steganography Tool')
    subparsers = parser.add_subparsers(dest='command')

    enc = subparsers.add_parser('encode', help='Embed a text message into a WAV file')
    enc.add_argument('input_wav', help='Path to original WAV file')
    enc.add_argument('message', help='Text message to embed')
    enc.add_argument('output_wav', help='Path to output stego WAV file')

    dec = subparsers.add_parser('decode', help='Extract hidden message from a stego WAV file')
    dec.add_argument('stego_wav', help='Path to stego WAV file')

    args = parser.parse_args()

    if args.command == 'encode':
        embed_message(args.input_wav, args.message, args.output_wav)
        print(f'✅ Message embedded into {args.output_wav}')
    elif args.command == 'decode':
        try:
            message = extract_message(args.stego_wav)
            print('✅ Decoded Message:', message)
        except Exception as e:
            print(f'❌ Error: {e}')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
