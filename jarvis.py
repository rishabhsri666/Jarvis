import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import pyttsx3
import webbrowser
from datetime import datetime
import requests
import subprocess
import re

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

conversation_history = []

SYSTEM_PROMPT = """
You are Jarvis, a helpful AI assistant.

You remember previous conversation messages.

If the user tells you their name, remember it.

Reply naturally and briefly.
"""

def ask_ai(prompt):

    conversation_history.append(
        f"User: {prompt}"
    )

    full_prompt = SYSTEM_PROMPT + "\n\n"

    for message in conversation_history:
        full_prompt += message + "\n"

    full_prompt += "Assistant:"

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": full_prompt,
            "stream": False
        }
    )

    data = response.json()

    reply = data["response"].strip()

    # cleanup
    reply = reply.replace("Assistant:", "")
    reply = reply.replace("Jarvis:", "")
    reply = reply.strip()

    conversation_history.append(
        f"Assistant: {reply}"
    )

    return reply


# -----------------------------------
# LOAD WHISPER
# -----------------------------------

print("Loading Whisper model...")

model = WhisperModel("small")

print("Jarvis is ready.")

# -----------------------------------
# SETTINGS
# -----------------------------------

sample_rate = 16000
duration = 5

# -----------------------------------
# APP MAPPINGS
# -----------------------------------

apps = {
    "calculator": "calc.exe",
    "powershell": "powershell.exe",
    "chrome": "chrome.exe",
    "notepad": "notepad.exe",
    "paint": "mspaint.exe",
    "spotify": "spotify.exe",
    "vscode": "code"
}


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

    segments, info = model.transcribe(
        "voice.wav",
        language="en"
    )

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

    # -----------------------------------
    # OPEN APPLICATIONS
    # -----------------------------------

    elif command.startswith("open"):

        app = command.replace("open", "").strip()

        # remove punctuation
        app = re.sub(r'[^\w\s]', '', app)

        if app in apps:

            speak(f"Opening {app}")

            try:

                subprocess.Popen(apps[app])

            except:

                speak("Could not open application")

        else:

            speak("Application not found")

    # -----------------------------------
    # EXIT
    # -----------------------------------

    elif "exit" in command:

        speak("Goodbye")

        break

    # -----------------------------------
    # AI MODE
    # -----------------------------------

    else:

        speak("Thinking")

        try:

            reply = ask_ai(command)

            # print("\nAI:", reply)

            speak(reply)

        except:

            speak("AI connection failed")