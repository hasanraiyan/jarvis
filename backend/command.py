import time
import pyttsx3
import speech_recognition as sr
import eel

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    # print(voices)
    engine.setProperty('voice', voices[2].id)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()
    engine.setProperty('rate', 174)
    eel.receiverText(text)

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm listening...")
        eel.DisplayMessage("I'm listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 8)

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
        # Don't speak back the user's input
        eel.DisplayMessage(f"You said: {query}")
    except Exception as e:
        print(f"Error: {str(e)}\n")
        return None

    return query.lower()

@eel.expose
def takeAllCommands(message=None):
    if message is None:
        query = takecommand()  # If no message is passed, listen for voice input
        if not query:
            return {'value': ''}  # Return empty string instead of None to avoid KeyError
        print(query)
        eel.senderText(query)
    else:
        query = message  # If there's a message, use it
        print(f"Message received: {query}")
        eel.senderText(query)

    ai_response = ""
    try:
        if query:
            if "open" in query:
                from backend.feature import openCommand
                openCommand(query)
                ai_response = f"Opening {query.replace('open', '').strip()}"
            elif "send message" in query or "call" in query or "video call" in query:
                from backend.feature import findContact, whatsApp
                flag = ""
                Phone, name = findContact(query)
                if Phone != 0:
                    if "send message" in query:
                        flag = 'message'
                        speak("What message to send?")
                        message_text = takecommand()  # Ask for the message text
                        whatsApp(Phone, message_text, flag, name)
                        ai_response = f"Message sent to {name}"
                    elif "call" in query:
                        flag = 'call'
                        whatsApp(Phone, query, flag, name)
                        ai_response = f"Calling {name}"
                    else:
                        flag = 'video call'
                        whatsApp(Phone, query, flag, name)
                        ai_response = f"Starting video call with {name}"
                else:
                    ai_response = "Contact not found"
            elif "on youtube" in query:
                from backend.feature import PlayYoutube
                PlayYoutube(query)
                ai_response = f"Playing on YouTube"
            else:
                from backend.feature import chatBot
                ai_response = chatBot(query)
            
            # Save chat to history
            if query and ai_response:
                from backend.db import save_chat_message
                if save_chat_message(query, ai_response):
                    print("Chat saved to history")
        else:
            speak("No command was given.")
            ai_response = "No command was given."
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, something went wrong.")
        ai_response = "Sorry, something went wrong."

    eel.ShowHood()
    return {'value': query}  # Return query string as 'value' to frontend

@eel.expose
def getChatHistory():
    """Get chat history for frontend"""
    from backend.db import get_chat_history
    return get_chat_history()

@eel.expose
def clearChatHistory():
    """Clear chat history"""
    from backend.db import clear_chat_history
    result = clear_chat_history()
    if result:
        speak("Chat history cleared")
    return result

@eel.expose
def initializeChatHistory():
    """Initialize chat history on startup"""
    from backend.db import get_chat_history
    try:
        # Just test the connection
        get_chat_history(1)
        return True
    except Exception as e:
        print(f"Error initializing chat history: {e}")
        return False@ee
l.expose
def getChatContextSettings():
    """Get current chat context settings"""
    from backend.openai_config import CHAT_HISTORY_CONTEXT_LIMIT, USE_CHAT_HISTORY
    return {
        'enabled': USE_CHAT_HISTORY,
        'context_limit': CHAT_HISTORY_CONTEXT_LIMIT
    }

@eel.expose
def toggleChatContext():
    """Toggle chat history context on/off"""
    # Note: This would require modifying the config file or using a database setting
    # For now, just return current status
    from backend.openai_config import USE_CHAT_HISTORY
    return USE_CHAT_HISTORY