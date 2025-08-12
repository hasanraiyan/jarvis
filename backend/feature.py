import os
import re
from shlex import quote
import struct
import subprocess
import time
import webbrowser
import eel
import openai
import pvporcupine
import pyaudio
import pyautogui
import pywhatkit as kit
import pygame
from backend.command import speak
from backend.config import ASSISTANT_NAME
import sqlite3

from backend.helper import extract_yt_term, remove_words

conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()

# Initialize pygame mixer
pygame.mixer.init()

@eel.expose
def play_assistant_sound():
    # Build relative path to start_sound.mp3
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # two levels up from backend/feature.py
    sound_file = os.path.join(base_dir, "frontend", "assets", "audio", "start_sound.mp3")

    if os.path.exists(sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    else:
        print(f"Sound file not found: {sound_file}")

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "").replace("open", "").lower()
    app_name = query.strip()

    if app_name != "":
        try:
            cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if results:
                speak("Opening " + query)
                os.startfile(results[0][0])
            else:
                cursor.execute('SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()

                if results:
                    speak("Opening " + query)
                    webbrowser.open(results[0][0])
                else:
                    speak("Opening " + query)
                    try:
                        os.system('start ' + query)
                    except Exception:
                        speak("Not found")
        except Exception:
            speak("Something went wrong")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing " + search_term + " on YouTube")
    kit.playonyt(search_term)

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)

        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)

            if keyword_index >= 0:
                print("hotword detected")
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")

    except Exception:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT Phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except Exception:
        speak('Not exist in contacts')
        return 0, 0

def whatsApp(Phone, message, flag, name):
    if flag == 'message':
        target_tab = 12
        jarvis_message = "Message sent successfully to " + name
    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "Calling to " + name
    else:
        target_tab = 6
        message = ''
        jarvis_message = "Starting video call with " + name

    encoded_message = quote(message)
    whatsapp_url = f"whatsapp://send?phone={Phone}&text={encoded_message}"
    full_command = f'start "" "{whatsapp_url}"'

    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)

    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

def chatBot(query):
    from backend.openai_config import (
        OPENAI_API_KEY, 
        OPENAI_API_BASE, 
        DEFAULT_MODEL, 
        MAX_TOKENS, 
        TEMPERATURE, 
        SYSTEM_MESSAGE
    )
    
    if not OPENAI_API_KEY:
        speak("OpenAI API key is not set. Please configure it in your environment variables.")
        return "Error: OpenAI API key not configured"
    
    user_input = query.lower()
    
    try:
        # Initialize the client with configurations
        client = openai.OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_API_BASE
        )
        
        # Create chat completion with the new client
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": user_input}
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )
        
        # Access response content with the new structure
        ai_response = response.choices[0].message.content.strip()
        print(ai_response)
        speak(ai_response)
        return ai_response
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        speak(error_message)
        return error_message
