import json
import vosk
import sys
import os
import queue
import sounddevice as sd

class SpeechToText:
    def __init__(self):
        # Check if model exists
        if not os.path.exists("model"):
            print("Please download the model from https://alphacephei.com/vosk/models")
            print("and unpack it as 'model' in the current folder.")
            sys.exit(1)
            
        # Initialize Vosk model
        print("Loading model...")
        self.model = vosk.Model("model")
        print("Model loaded successfully!")
        
        self.samplerate = 16000
        self.q = queue.Queue()
        
        # Print available audio devices
        print("\nAvailable audio devices:")
        print(sd.query_devices())
        
        # Find USB microphone
        devices = sd.query_devices()
        self.device_id = None
        for i, device in enumerate(devices):
            if 'USB Audio' in device['name'] and device['max_input_channels'] > 0:
                self.device_id = i
                print(f"\nSelected microphone: {device['name']}")
                break
        
        if self.device_id is None:
            print("\nNo USB microphone found. Using default input device.")
            self.device_id = sd.default.device[0]

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def real_time_transcribe(self):
        """Real-time transcription from microphone"""
        try:
            # Create recognizer
            rec = vosk.KaldiRecognizer(self.model, self.samplerate)
            rec.SetWords(True)  # Enable word-level output

            # Start recording
            print("\nListening... Press Ctrl+C to stop")
            print("Speak now!")
            print("-" * 50)
            
            with sd.RawInputStream(device=self.device_id,
                                 samplerate=self.samplerate, 
                                 blocksize=8000, 
                                 dtype='int16', 
                                 channels=1, 
                                 callback=self.callback):
                while True:
                    data = self.q.get()
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        text = result.get("text", "").strip()
                        if text:
                            print("\nFinal:", text)
                    else:
                        partial = json.loads(rec.PartialResult())
                        text = partial.get("partial", "").strip()
                        if text:
                            print("\rPartial:", text, end='', flush=True)

        except KeyboardInterrupt:
            print("\nStopped listening.")
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please check if your microphone is properly connected and selected as the default input device.")
            print("You can try selecting a different input device from the list shown above.")

def main():
    stt = SpeechToText()
    try:
        while True:
            print("\nSpeech to Text Menu:")
            print("1. Start real-time transcription")
            print("2. Exit")
            choice = input("Enter your choice (1-2): ")
            
            if choice == "1":
                stt.real_time_transcribe()
            elif choice == "2":
                break
            else:
                print("Invalid choice. Please try again.")
                
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main() 