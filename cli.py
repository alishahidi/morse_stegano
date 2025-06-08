import argparse
import logging
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.logging import RichHandler
from rich import print as rprint
from steg_core import (
    embed_message,
    extract_message,
    SteganographyError,
    MessageTooLongError,
    InvalidAudioFileError,
    MessageNotFoundError
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("audio_steganography")

console = Console()

def print_error(message: str) -> None:
    """Print an error message in a nice format."""
    console.print(Panel(message, title="[red]Error[/red]", border_style="red"))

def print_success(message: str) -> None:
    """Print a success message in a nice format."""
    console.print(Panel(message, title="[green]Success[/green]", border_style="green"))

def print_info(message: str) -> None:
    """Print an info message in a nice format."""
    console.print(Panel(message, title="[blue]Info[/blue]", border_style="blue"))

def validate_file_path(file_path: str, check_exists: bool = True) -> Path:
    """Validate and return a Path object for the given file path."""
    path = Path(file_path)
    if check_exists and not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if not path.suffix.lower() == '.wav':
        raise ValueError("File must be a WAV file")
    return path

def main():
    parser = argparse.ArgumentParser(
        description='🔊 Morse Code Audio Steganography Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Hide a message in an audio file
  python cli.py encode input.wav "Secret message" output.wav

  # Extract a hidden message
  python cli.py decode stego.wav
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Encode command
    enc = subparsers.add_parser('encode', help='Embed a text message into a WAV file')
    enc.add_argument('input_wav', help='Path to original WAV file')
    enc.add_argument('message', help='Text message to embed')
    enc.add_argument('output_wav', help='Path to output stego WAV file')

    # Decode command
    dec = subparsers.add_parser('decode', help='Extract hidden message from a stego WAV file')
    dec.add_argument('stego_wav', help='Path to stego WAV file')

    args = parser.parse_args()

    try:
        if args.command == 'encode':
            # Validate input file
            input_path = validate_file_path(args.input_wav)
            output_path = validate_file_path(args.output_wav, check_exists=False)
            
            # Show progress
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console
            ) as progress:
                task = progress.add_task("[cyan]Embedding message...", total=100)
                
                # Log the process
                log.info(f"Reading input file: {input_path}")
                log.info(f"Message length: {len(args.message)} characters")
                
                # Embed the message
                embed_message(str(input_path), args.message, str(output_path))
                
                # Update progress
                progress.update(task, completed=100)
            
            print_success(f"Message successfully embedded into {output_path}")
            log.info("Process completed successfully")
            
        elif args.command == 'decode':
            # Validate input file
            stego_path = validate_file_path(args.stego_wav)
            
            # Show progress
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console
            ) as progress:
                task = progress.add_task("[cyan]Extracting message...", total=100)
                
                # Log the process
                log.info(f"Reading stego file: {stego_path}")
                
                # Extract the message
                message = extract_message(str(stego_path))
                
                # Update progress
                progress.update(task, completed=100)
            
            print_success(f"Decoded Message: {message}")
            log.info("Process completed successfully")
            
        else:
            parser.print_help()
            
    except FileNotFoundError as e:
        print_error(str(e))
        log.error("File not found")
    except MessageTooLongError as e:
        print_error(str(e))
        log.error("Message too long for the audio file")
    except InvalidAudioFileError as e:
        print_error(str(e))
        log.error("Invalid audio file")
    except MessageNotFoundError as e:
        print_error(str(e))
        log.error("No message found in the audio file")
    except SteganographyError as e:
        print_error(f"Steganography error: {str(e)}")
        log.error("Steganography error occurred")
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        log.error("Unexpected error occurred", exc_info=True)

if __name__ == '__main__':
    main()
