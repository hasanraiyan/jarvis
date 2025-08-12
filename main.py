import os
import eel
from backend.auth import recognise
from backend.auth.recognise import AuthenticateFace, SetupFaceAuth
from backend.db import is_face_setup
from backend.feature import *
from backend.command import *

def start():
    eel.init("frontend") 
    play_assistant_sound()
    
    @eel.expose
    def init():
        eel.hideLoader()
        speak("Welcome to Jarvis")
        
        # Check if face authentication is set up
        if not is_face_setup():
            speak("Face authentication not set up. Please complete the setup process.")
            eel.showFaceSetup()
        else:
            speak("Ready for Face Authentication")
            eel.showFaceAuth()
            flag = AuthenticateFace()
            if flag == 1:
                speak("Face recognized successfully")
                eel.hideFaceAuth()
                eel.showFaceAuthSuccess()
                speak("Welcome to Your Assistant")
                eel.hideStart()
                play_assistant_sound()
            elif flag == 0:
                speak("Face authentication not set up properly. Please complete setup.")
                eel.hideFaceAuth()
                eel.showFaceSetup()
            else:
                speak("Face not recognized. Please try again")
                eel.hideFaceAuth()
                eel.showFaceSetup()
    
    @eel.expose
    def setup_face_auth():
        """Handle face authentication setup"""
        try:
            speak("Starting face authentication setup")
            success = SetupFaceAuth()
            if success:
                speak("Face authentication setup completed successfully")
                return {"success": True, "message": "Setup completed successfully"}
            else:
                speak("Face authentication setup failed. Please try again")
                return {"success": False, "message": "Setup failed. Please try again"}
        except Exception as e:
            print(f"Error in face setup: {e}")
            return {"success": False, "message": "Setup error occurred"}
    
    @eel.expose
    def setup_face_auth_with_images(image_data_list):
        """Handle face authentication setup with images from frontend"""
        try:
            speak("Processing captured images")
            from backend.auth.recognise import SetupFaceAuthWithImages
            success = SetupFaceAuthWithImages(image_data_list)
            if success:
                speak("Face authentication setup completed successfully")
                return {"success": True, "message": "Setup completed successfully"}
            else:
                speak("Face authentication setup failed. Please try again")
                return {"success": False, "message": "Setup failed. Please try again"}
        except Exception as e:
            print(f"Error in face setup with images: {e}")
            return {"success": False, "message": "Setup error occurred"}
    
    @eel.expose
    def authenticate_face():
        """Handle face authentication"""
        try:
            flag = AuthenticateFace()
            if flag == 1:
                speak("Face recognized successfully")
                eel.hideFaceAuth()
                eel.showFaceAuthSuccess()
                speak("Welcome to Your Assistant")
                eel.hideStart()
                play_assistant_sound()
                return {"success": True, "message": "Authentication successful"}
            elif flag == 0:
                speak("Face authentication not set up properly")
                eel.showAuthRetryButtons()
                return {"success": False, "message": "Face authentication not set up"}
            else:
                speak("Face not recognized. Please try again")
                eel.showAuthRetryButtons()
                return {"success": False, "message": "Authentication failed"}
        except Exception as e:
            print(f"Error in face authentication: {e}")
            eel.showAuthRetryButtons()
            return {"success": False, "message": "Authentication error occurred"}
    
    @eel.expose
    def skip_face_setup():
        """Skip face setup for now"""
        speak("Face authentication skipped. You can set it up later in settings.")
        eel.hideFaceSetup()
        eel.hideStart()
        play_assistant_sound()
        return {"success": True, "message": "Setup skipped"}
    
    @eel.expose
    def reset_face_auth():
        """Reset face authentication setup"""
        try:
            from backend.db import reset_face_setup
            import shutil
            
            # Reset database flag
            reset_face_setup()
            
            # Remove sample images and trainer
            if os.path.exists('backend/auth/samples'):
                shutil.rmtree('backend/auth/samples')
            if os.path.exists('backend/auth/trainer'):
                shutil.rmtree('backend/auth/trainer')
            
            speak("Face authentication has been reset")
            return {"success": True, "message": "Face authentication reset successfully"}
        except Exception as e:
            print(f"Error resetting face auth: {e}")
            return {"success": False, "message": "Error resetting face authentication"}
        
    os.system('start msedge.exe --app="http://127.0.0.1:8000/index.html"')
    eel.start("index.html", mode=None, host="localhost", block=True) 