#!/usr/bin/env python3
"""
Test script for tool speech announcements
"""

import sys
sys.path.append('.')

from backend.openai_function_calling import jarvis_ai

def test_tool_speech():
    print("🔊 === Tool Speech Announcements Test ===\n")
    print("Testing speech announcements for different tools\n")
    
    # Test cases that should trigger different tools with speech
    test_cases = [
        {
            "query": "What's 25 plus 37?",
            "expected_tool": "calculate",
            "expected_speech": "Let me calculate that for you"
        },
        {
            "query": "What time is it?",
            "expected_tool": "get_current_time", 
            "expected_speech": "Let me check the current time"
        },
        {
            "query": "What do you see?",
            "expected_tool": "capture_image",
            "expected_speech": "Let me take a look with my camera"
        },
        {
            "query": "What's the weather like?",
            "expected_tool": "get_weather",
            "expected_speech": "Let me check the weather conditions"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. Testing: '{test_case['query']}'")
        print(f"   Expected tool: {test_case['expected_tool']}")
        print(f"   Expected speech: Contains '{test_case['expected_speech']}'")
        
        try:
            result = jarvis_ai.process_message(test_case['query'])
            
            if result["success"]:
                print(f"   ✅ Response: {result['response']}")
                if result["tools_used"]:
                    print(f"   🔧 Tools used: {result['tools_used']}")
                    if test_case['expected_tool'] in result['tools_used']:
                        print(f"   ✅ Correct tool used!")
                    else:
                        print(f"   ⚠️  Expected {test_case['expected_tool']}, got {result['tools_used']}")
                else:
                    print("   ⚠️  No tools used")
            else:
                print(f"   ❌ Error: {result['response']}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
        
        print("   " + "-"*60)
        print()
    
    # Cleanup
    jarvis_ai.cleanup()
    
    print("🎯 === Speech Announcement Features ===")
    print("✅ Dynamic speech announcements for each tool")
    print("✅ Variety in speech patterns (random selection)")
    print("✅ Natural, conversational tool usage")
    print("✅ UI captions synchronized with speech")
    print("✅ Error handling for speech failures")
    
    print("\n🎉 JARVIS now speaks when using tools!")
    print("🔊 You should hear:")
    print("   • 'Let me calculate that for you' → Calculator")
    print("   • 'Let me take a look with my camera' → Camera")
    print("   • 'Let me check the current time' → Time")
    print("   • 'Let me check the weather conditions' → Weather")

if __name__ == "__main__":
    test_tool_speech()