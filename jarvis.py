import os
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import pyttsx3
import webbrowser
from datetime import datetime

# -----------------------------
# TEXT TO SPEECH
# -----------------------------
engine = pyttsx3.init()

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# -----------------------------
# WHISPER MODEL
# -----------------------------
print("Loading Whisper model...")

model = WhisperModel("base")

print("Jarvis is ready.")

sample_rate = 44100
duration = 5

# -----------------------------
# MAIN LOOP
# -----------------------------
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

    command = command.lower()

    print("\nYou said:", command)

    # -----------------------------
    # COMMANDS
    # -----------------------------

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

    elif "spotify" in command:
        speak("Opening Spotify")
        os.system("start spotify")

    elif "chrome" in command:
        speak("Opening Chrome")
        os.system("start chrome")

    elif "exit" in command:
        speak("Goodbye")
        break

    else:
        speak("I did not understand")