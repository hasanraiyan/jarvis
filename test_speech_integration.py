#!/usr/bin/env python3
"""
Test speech integration with JARVIS
"""

import sys
sys.path.append('.')

from backend.command import speak
from backend.openai_function_calling import jarvis_ai

def test_speech_integration():
    print("🔊 === Speech Integration Test ===\n")
    
    # Test basic speech
    print("1. Testing basic speech...")
    speak("Hello, this is a speech test.")
    
    print("\n2. Testing AI response with speech...")
    
    # Test AI response
    result = jarvis_ai.process_message("What's 10 plus 5?")
    
    if result["success"]:
        print(f"AI Response: {result['response']}")
        print("Speaking the response...")
        speak(result["response"])
        
        if result["tools_used"]:
            print(f"Tools used: {result['tools_used']}")
    else:
        print(f"Error: {result['response']}")
    
    print("\n✅ Speech integration test complete!")

if __name__ == "__main__":
    test_speech_integration()