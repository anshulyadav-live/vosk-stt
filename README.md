# Local Speech-to-Text Application

This is a local, offline speech-to-text application using Vosk. It works completely on your computer without requiring an internet connection.

## Prerequisites

- Python 3.7 or higher
- A working microphone
- Windows operating system

## Setup Instructions

1. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

2. Download a Vosk model:
   - Go to https://alphacephei.com/vosk/models
   - Download a model (recommended: `vosk-model-small-en-us-0.15`)
   - Extract the downloaded model folder
   - Rename the extracted folder to `model` and place it in the same directory as the script

## Usage

1. Run the script:
   ```
   python speech_to_text.py
   ```

2. Choose option 1 to start recording
3. Speak into your microphone
4. Press Ctrl+C to stop recording
5. The transcription will appear automatically

## Features

- Completely offline operation
- Real-time transcription
- Simple command-line interface
- Supports multiple languages (depending on the model used)

## Notes

- The accuracy of transcription depends on the model you choose. Larger models generally provide better accuracy but require more disk space.
- Make sure your microphone is properly connected and set as the default input device.
- The application saves recordings as WAV files in the current directory. 
