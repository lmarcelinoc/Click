import os
import json
import pyttsx3
import pyaudio
import wave
from vosk import Model, KaldiRecognizer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
model_path = os.getenv("VOSK_MODEL_PATH")
input_device_index = int(os.getenv("INPUT_DEVICE_INDEX", '3'))  # Use a default if not set

if not os.path.exists(model_path):
    print("Model path is incorrect. Please check your VOSK_MODEL_PATH in the .env file.")
    exit(1)

# Initialize Vosk model
model = Model(model_path)
rec = KaldiRecognizer(model, 32000)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

def speak(text):
    """Convert text to speech using pyttsx3."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    """Capture audio from the microphone and convert it to text using Vosk."""
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=32000, input=True, input_device_index=input_device_index, frames_per_buffer=4000)
    stream.start_stream()
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            return result.get('text', '')

def main():
    """Main function to handle the speech interaction loop."""
    print("Say something...")
    while True:
        spoken_text = listen()
        if spoken_text:
            print("You said:", spoken_text)
            speak("You said " + spoken_text)
        else:
            print("I didn't catch that.")
            speak("I didn't catch that.")

    # Close the PyAudio stream and terminate the program
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    main()
