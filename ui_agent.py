import os
import json
import pyttsx3
import pyaudio
from vosk import Model, KaldiRecognizer
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
model_path = os.getenv("VOSK_MODEL_PATH")
input_device_index = int(os.getenv("INPUT_DEVICE_INDEX", '3'))  # Default to device index 3 if not set
openrouter_endpoint = os.getenv("OPENROUTER_ENDPOINT")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

if not os.path.exists(model_path):
    print("Model path is incorrect. Please check your VOSK_MODEL_PATH in the .env file.")
    exit(1)

# Initialize Vosk model and PyAudio
model = Model(model_path)
rec = KaldiRecognizer(model, 32000)
p = pyaudio.PyAudio()

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

# Setup OpenAI client with OpenRouter
client = OpenAI(
  base_url=openrouter_endpoint,
  api_key=openrouter_api_key
)

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
            spoken_text = result.get('text', '')
            if "goodbye" in spoken_text.lower():  # Check if the user wants to end the conversation
                return "EXIT"
            return spoken_text

def get_llm_response(input_text):
    """Send text to OpenRouter and get the response."""
    completion = client.chat.completions.create(
      extra_headers={
        "HTTP-Referer": os.getenv("YOUR_SITE_URL"),
        "X-Title": os.getenv("YOUR_APP_NAME"),
      },
      model="openai/gpt-3.5-turbo",
      messages=[{"role": "user", "content": input_text}]
    )
    return completion.choices[0].message.content

def main():
    """Main function to handle the speech interaction loop."""
    print("Say something...")
    while True:
        spoken_text = listen()
        if spoken_text == "exit":
            print("Goodbye!")
            speak("Goodbye!")
            break
        elif spoken_text:
            print("You said:", spoken_text)
            response = get_llm_response(spoken_text)
            print("Response from LLM:", response)
            speak(response)
        else:
            print("I didn't catch that.")
            speak("I didn't catch that.")

    # Cleanup PyAudio resources
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    main()
