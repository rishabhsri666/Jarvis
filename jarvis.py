import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import pyttsx3
import webbrowser
from datetime import datetime
import requests
import os

# -----------------------------------
# TEXT TO SPEECH
# -----------------------------------


def speak(text):

    print("\nJarvis:", text)

    engine = pyttsx3.init()

    engine.say(text)

    engine.runAndWait()

    engine.stop()

# -----------------------------------
# AI FUNCTION
# -----------------------------------

def ask_ai(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data["response"]

# -----------------------------------
# LOAD WHISPER
# -----------------------------------

print("Loading Whisper model...")

model = WhisperModel("base")

print("Jarvis is ready.")

sample_rate = 44100
duration = 5

# -----------------------------------
# MAIN LOOP
# -----------------------------------

while True:

    input("\nPress ENTER to talk...")

    print("Listening...")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='int16'
    )

    sd.wait()

    write("voice.wav", sample_rate, recording)

    print("Processing...")

    segments, info = model.transcribe("voice.wav")

    command = ""

    for segment in segments:
        command += segment.text

    command = command.lower().strip()

    print("\nYou said:", command)

    # -----------------------------------
    # BASIC COMMANDS
    # -----------------------------------

    if "hello" in command:
        speak("Hello Rishabh")

    elif "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "notepad" in command:
        speak("Opening Notepad")
        os.system("start notepad")

    elif "calculator" in command:
        speak("Opening Calculator")
        os.system("start calc")

    elif "exit" in command:
        speak("Goodbye")
        break

    # -----------------------------------
    # AI MODE
    # -----------------------------------

    else:

        speak("Thinking")

        reply = ask_ai(command)

        # print("\nAI:", reply)

        speak(reply)