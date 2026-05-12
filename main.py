from commands.apps import *
from commands.system import *
from commands.router import detect_intent
from commands.web import *


import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import pyttsx3
from datetime import datetime
import requests
import re
import numpy as np


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
# MEMORY
# -----------------------------------

conversation_history = []

SYSTEM_PROMPT = """
You are Jarvis, a helpful AI assistant.

You remember previous conversation messages.

If the user tells you their name, remember it.

Reply naturally and briefly.
"""


# -----------------------------------
# AI FUNCTION
# -----------------------------------

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


# -----------------------------------
# MAIN LOOP
# -----------------------------------

while True:

    input("\nPress ENTER to talk...")

    print("Listening...")

    recording = []

    silence_threshold = 1000
    silence_duration = 1.5
    max_duration = 10

    silent_chunks = 0
    total_chunks = 0

    with sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        dtype='int16'
    ) as stream:

        while True:

            audio_chunk, overflowed = stream.read(1024)

            recording.append(audio_chunk)

            volume = np.abs(audio_chunk).mean()

            total_chunks += 1

            # silence detection
            if volume < silence_threshold:

                silent_chunks += 1

            else:

                silent_chunks = 0

            # stop after silence
            if silent_chunks > (silence_duration * sample_rate / 1024):

                break

            # force stop
            if total_chunks > (max_duration * sample_rate / 1024):

                break

    audio = np.concatenate(recording)

    write("voice.wav", sample_rate, audio)

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
    # DETECT INTENT
    # -----------------------------------

    intent = detect_intent(command)

    print("Intent:", intent)

    # -----------------------------------
    # TIME
    # -----------------------------------

    if intent == "time":

        current_time = datetime.now().strftime("%I:%M %p")

        speak(f"The time is {current_time}")

    # -----------------------------------
    # OPEN APPS / WEBSITES
    # -----------------------------------

    elif intent == "open":

        words = command.split()

        target = " ".join(words[1:])

        target = re.sub(r'[^\w\s]', '', target)

        success = (
            open_app(target)
            or open_website(target)
            or open_folder(target)
        )

        if success:

            speak(f"Opening {target}")

        else:

            speak("Application, website, or folder not found")

    # -----------------------------------
    # SYSTEM COMMANDS
    # -----------------------------------

    elif intent == "battery":

        battery_status = get_battery()

        speak(battery_status)

    elif intent == "shutdown":

        speak("Shutting down computer")

        shutdown_pc()

    elif intent == "restart":

        speak("Restarting computer")

        restart_pc()

    elif intent == "lock":

        speak("Locking computer")

        lock_pc()
        
        # -----------------------------------
    # GOOGLE SEARCH
    # -----------------------------------

    elif intent == "google_search":

        query = command.replace(
            "search google for",
            ""
        ).strip()

        speak(f"Searching Google for {query}")

        google_search(query)


    # -----------------------------------
    # YOUTUBE SEARCH
    # -----------------------------------

    elif intent == "youtube_search":

        query = command.replace(
            "search youtube for",
            ""
        ).strip()

        speak(f"Searching YouTube for {query}")

        youtube_search(query)

    # -----------------------------------
    # EXIT
    # -----------------------------------

    elif intent == "exit":

        speak("Goodbye")

        break

    # -----------------------------------
    # AI MODE
    # -----------------------------------

    else:

        speak("Thinking")

        try:

            reply = ask_ai(command)

            speak(reply)

        except:

            speak("AI connection failed")