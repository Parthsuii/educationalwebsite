import openai
import os
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
load_dotenv()

# OpenAI API Key (Replace with your own key)
OPENAI_API_KEY = os.getenv("")
print(f"API Key Loaded: {OPENAI_API_KEY}")
# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Speed of speech
engine.setProperty("volume", 1)  # Volume level

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture audio and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that.")
        except sr.RequestError:
            speak("Could not connect to speech recognition service.")
        return None
def get_response(prompt):
    """Get AI-generated response using OpenAI GPT."""
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return "Sorry, I am unable to process your request right now."

def assistant():
    """Main voice assistant loop."""
    speak("Hello! How can I assist you?")
    while True:
        command = listen()
        if command:
            if "stop" in command or "exit" in command:
                speak("Goodbye! Have a great day.")
                break
            else:
                response = get_response(command)
                speak(response)

if __name__ == "__main__":
    assistant()