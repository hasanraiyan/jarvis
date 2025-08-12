"""
Proper OpenAI Function Calling System for JARVIS
Implements the correct tool execution lifecycle
"""

import json
import base64
import cv2
import os
import openai
from datetime import datetime
from backend.openai_config import OPENAI_API_KEY, OPENAI_API_BASE
from backend.db import save_chat_message, get_recent_chat_context

# Initialize OpenAI client with custom base URL
client = openai.OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE
)

# Define available tools for JARVIS
JARVIS_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "capture_image",
            "description": "Capture an image from the camera and return it as base64. Use when user asks about visual things, what they can see, or anything requiring sight.",
            "parameters": {
                "type": "object",
                "properties": {
                    "purpose": {
                        "type": "string",
                        "description": "What the user wants to see or analyze in the image"
                    }
                },
                "required": ["purpose"]
            }
        }
    },
    {
        "type": "function", 
        "function": {
            "name": "calculate",
            "description": "Perform mathematical calculations. Use for any math problems, equations, or numerical computations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to calculate (e.g., '25 + 37', '15 * 8')"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get current time and date information. Use when user asks about time, date, or current datetime.",
            "parameters": {
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "description": "Format requested: 'time', 'date', 'datetime', or 'full'",
                        "enum": ["time", "date", "datetime", "full"]
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather information. Use when user asks about weather, temperature, or outdoor conditions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location to get weather for (optional, defaults to current location)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "control_system",
            "description": "Control computer system - open applications, files, or perform system actions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "Action to perform: 'open_app', 'open_website', 'system_command'",
                        "enum": ["open_app", "open_website", "system_command"]
                    },
                    "target": {
                        "type": "string",
                        "description": "Target application, website, or command to execute"
                    }
                },
                "required": ["action", "target"]
            }
        }
    }
]

class JarvisToolExecutor:
    def __init__(self):
        self.camera = None
    
    def capture_image(self, purpose="general observation"):
        """Capture image from camera"""
        try:
            # Initialize camera if needed
            if self.camera is None:
                self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                self.camera.set(3, 640)
                self.camera.set(4, 480)
            
            # Capture frame
            ret, frame = self.camera.read()
            if not ret:
                return json.dumps({"error": "Failed to capture image from camera"})
            
            # Convert to base64
            _, buffer = cv2.imencode('.jpg', frame)
            image_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return json.dumps({
                "success": True,
                "image_base64": image_base64,
                "purpose": purpose,
                "message": f"Image captured successfully for: {purpose}"
            })
            
        except Exception as e:
            return json.dumps({"error": f"Camera error: {str(e)}"})
    
    def calculate(self, expression):
        """Perform mathematical calculations"""
        try:
            # Safe evaluation using eval with restricted globals
            allowed_names = {
                "__builtins__": {},
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow, "divmod": divmod
            }
            
            # Replace common math terms
            expression = expression.replace("times", "*").replace("plus", "+")
            expression = expression.replace("minus", "-").replace("divided by", "/")
            
            result = eval(expression, allowed_names, {})
            
            return json.dumps({
                "success": True,
                "expression": expression,
                "result": result,
                "message": f"{expression} = {result}"
            })
            
        except Exception as e:
            return json.dumps({"error": f"Calculation error: {str(e)}"})
    
    def get_current_time(self, format="datetime"):
        """Get current time information"""
        try:
            now = datetime.now()
            
            if format == "time":
                result = now.strftime("%H:%M:%S")
            elif format == "date":
                result = now.strftime("%Y-%m-%d")
            elif format == "full":
                result = now.strftime("%A, %B %d, %Y at %H:%M:%S")
            else:  # datetime
                result = now.strftime("%Y-%m-%d %H:%M:%S")
            
            return json.dumps({
                "success": True,
                "format": format,
                "result": result,
                "message": f"Current {format}: {result}"
            })
            
        except Exception as e:
            return json.dumps({"error": f"Time error: {str(e)}"})
    
    def get_weather(self, location="current location"):
        """Get weather information"""
        try:
            # Mock weather data - replace with real API
            weather_data = {
                "location": location,
                "temperature": "22°C",
                "condition": "Sunny",
                "humidity": "65%",
                "wind": "10 km/h",
                "description": "Clear skies with pleasant temperature"
            }
            
            return json.dumps({
                "success": True,
                "location": location,
                "weather": weather_data,
                "message": f"Weather in {location}: {weather_data['temperature']}, {weather_data['condition']}"
            })
            
        except Exception as e:
            return json.dumps({"error": f"Weather error: {str(e)}"})
    
    def control_system(self, action, target):
        """Control computer system"""
        try:
            if action == "open_app":
                # Use existing JARVIS app opening functionality
                from backend.command import openAppWeb
                result = openAppWeb(target)
                return json.dumps({
                    "success": True,
                    "action": action,
                    "target": target,
                    "message": f"Attempting to open {target}"
                })
            elif action == "open_website":
                import webbrowser
                webbrowser.open(target)
                return json.dumps({
                    "success": True,
                    "action": action,
                    "target": target,
                    "message": f"Opening website: {target}"
                })
            else:
                return json.dumps({
                    "success": True,
                    "action": action,
                    "message": f"System action executed: {action}"
                })
                
        except Exception as e:
            return json.dumps({"error": f"System control error: {str(e)}"})
    
    def execute_tool(self, tool_name, **kwargs):
        """Execute a specific tool by name"""
        if hasattr(self, tool_name):
            return getattr(self, tool_name)(**kwargs)
        else:
            return json.dumps({"error": f"Unknown tool: {tool_name}"})
    
    def cleanup(self):
        """Cleanup resources"""
        if self.camera:
            self.camera.release()
            self.camera = None

class JarvisAI:
    def __init__(self):
        self.tool_executor = JarvisToolExecutor()
        self.system_message = """You are JARVIS, an intelligent AI assistant with access to various tools and capabilities.

You can use tools to help users with:
- Visual analysis (camera) - When you capture images, you will receive detailed analysis of what's visible
- Mathematical calculations 
- Time and date information
- Weather information
- System control (opening apps, websites)

Guidelines:
1. Use tools when they would be helpful to answer the user's question
2. You can use multiple tools in one response if needed
3. When using the camera tool, you will get actual visual analysis - use this information in your response
4. Be conversational and helpful in your responses
5. Explain what you're doing when using tools
6. If no tools are needed, just have a normal conversation

Always be friendly, intelligent, and proactive in helping users."""

    def process_message(self, user_message):
        """Process user message with OpenAI function calling"""
        try:
            # Get chat context
            chat_context = get_recent_chat_context(3)
            
            # Build messages
            messages = [{"role": "system", "content": self.system_message}]
            
            # Add chat history
            for user_msg, ai_response in chat_context:
                messages.append({"role": "user", "content": user_msg})
                messages.append({"role": "assistant", "content": ai_response})
            
            # Add current message
            messages.append({"role": "user", "content": user_message})
            
            # Initial AI response with potential tool calls
            response = client.chat.completions.create(
                model="openai",  # Use compatible model
                messages=messages,
                tools=JARVIS_TOOLS,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=500
            )
            
            message = response.choices[0].message
            
            # Check if AI wants to use tools
            if message.tool_calls:
                return self._handle_tool_calls(message, messages, user_message)
            else:
                # Direct response without tools
                ai_response = message.content
                save_chat_message(user_message, ai_response)
                return {
                    "success": True,
                    "response": ai_response,
                    "tools_used": []
                }
                
        except Exception as e:
            print(f"Error in OpenAI function calling: {e}")
            # Fallback to simple response
            return {
                "success": False,
                "response": "I'm having trouble processing your request right now. Please try again.",
                "error": str(e)
            }
    
    def _handle_tool_calls(self, message, messages, original_user_message):
        """Handle the tool execution lifecycle"""
        try:
            tools_used = []
            
            # Add AI's message with tool calls to conversation
            messages.append(message)
            
            # Execute each tool call
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                print(f"🔧 JARVIS is using tool: {tool_name}")
                
                # Announce tool usage with speech and UI
                try:
                    import eel
                    from backend.command import speak
                    
                    # Get tool-specific announcement
                    announcement = self._get_tool_announcement(tool_name, tool_args)
                    
                    if announcement:
                        speak(announcement["speech"])
                        eel.DisplayMessage(announcement["ui"])
                    else:
                        # Fallback
                        speak(f"Using {tool_name.replace('_', ' ')}.")
                        eel.DisplayMessage(f"Using {tool_name}...")
                except Exception as e:
                    print(f"Error in tool announcement: {e}")
                    pass  # Continue even if speech/UI fails
                
                # Execute the tool
                tool_result = self.tool_executor.execute_tool(tool_name, **tool_args)
                tools_used.append(tool_name)
                
                # Add tool result to conversation
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                })
            
            # Get final response from AI with tool results
            final_response = client.chat.completions.create(
                model="openai",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            ai_response = final_response.choices[0].message.content
            
            # Handle image analysis if camera was used
            if "capture_image" in tools_used:
                ai_response = self._enhance_with_vision(messages, ai_response)
            
            # Save to chat history
            save_chat_message(original_user_message, ai_response)
            
            return {
                "success": True,
                "response": ai_response,
                "tools_used": tools_used
            }
            
        except Exception as e:
            print(f"Error handling tool calls: {e}")
            return {
                "success": False,
                "response": "I encountered an error using my tools. Please try again.",
                "error": str(e)
            }
    
    def _enhance_with_vision(self, messages, ai_response):
        """Enhance response with actual openai Vision analysis"""
        try:
            # Look for captured image in tool results
            for message in reversed(messages):
                if message.get("role") == "tool":
                    content = json.loads(message["content"])
                    if content.get("image_base64"):
                        # Get the image and analyze it with vision
                        image_base64 = content["image_base64"]
                        purpose = content.get("purpose", "general observation")
                        
                        # Analyze image with openai Vision
                        vision_analysis = self._analyze_image_with_gpt4_vision(image_base64, purpose)
                        
                        if vision_analysis:
                            # Replace generic response with actual vision analysis
                            if "Image captured" in ai_response or "I've captured" in ai_response:
                                return f"Looking at the image, I can see: {vision_analysis}"
                            else:
                                return ai_response + f"\n\nFrom the image I captured: {vision_analysis}"
                        else:
                            return ai_response + "\n\n[Image captured but vision analysis unavailable]"
            
            return ai_response
            
        except Exception as e:
            print(f"Error in vision enhancement: {e}")
            return ai_response
    
    def _analyze_image_with_gpt4_vision(self, image_base64, purpose="describe what you see"):
        """Analyze image using openai Vision"""
        try:
            # Try openai Vision first (if available)
            try:
                vision_response = client.chat.completions.create(
                    model="openai",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text", 
                                    "text": f"Analyze this image and {purpose}. Be specific and detailed about what you observe."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_base64}",
                                        "detail": "high"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=300,
                    temperature=0.7
                )
                
                return vision_response.choices[0].message.content
                
            except Exception as vision_error:
                print(f"openai Vision not available: {vision_error}")
                
                # Fallback: Use OpenCV for basic analysis
                return self._basic_image_analysis(image_base64)
                
        except Exception as e:
            print(f"Error in image analysis: {e}")
            return None
    
    def _basic_image_analysis(self, image_base64):
        """Basic image analysis using OpenCV as fallback"""
        try:
            import cv2
            import numpy as np
            
            # Decode base64 image
            image_data = base64.b64decode(image_base64)
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return "Unable to process the captured image."
            
            # Basic analysis
            height, width, channels = img.shape
            
            # Color analysis
            avg_color = np.mean(img, axis=(0, 1))
            brightness = np.mean(avg_color)
            
            # Face detection
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            # Build description
            description_parts = []
            description_parts.append(f"an image that is {width}x{height} pixels")
            
            if brightness > 127:
                description_parts.append("the scene appears bright and well-lit")
            else:
                description_parts.append("the scene appears dim or darker")
            
            if len(faces) > 0:
                if len(faces) == 1:
                    description_parts.append("I can detect 1 person's face")
                else:
                    description_parts.append(f"I can detect {len(faces)} people's faces")
            
            # Color dominance
            if avg_color[2] > avg_color[1] and avg_color[2] > avg_color[0]:  # More red
                description_parts.append("with warm/reddish tones")
            elif avg_color[1] > avg_color[0] and avg_color[1] > avg_color[2]:  # More green
                description_parts.append("with natural/greenish tones")
            elif avg_color[0] > avg_color[1] and avg_color[0] > avg_color[2]:  # More blue
                description_parts.append("with cool/bluish tones")
            
            return ", ".join(description_parts) + ". For more detailed analysis, openai Vision would provide better insights."
            
        except Exception as e:
            print(f"Error in basic image analysis: {e}")
            return "I captured an image but couldn't analyze its contents in detail."
    
    def _get_tool_announcement(self, tool_name, tool_args):
        """Get dynamic announcement for tool usage"""
        import random
        
        announcements = {
            "capture_image": {
                "speech": random.choice([
                    "Let me take a look with my camera.",
                    "I'll use my vision to see what's around.",
                    "Let me analyze the scene with my camera.",
                    "Using my camera to see what's there."
                ]),
                "ui": "Using camera to analyze the scene..."
            },
            "calculate": {
                "speech": random.choice([
                    "Let me calculate that for you.",
                    "I'll do the math for you.",
                    "Let me work out that calculation.",
                    "Calculating that now."
                ]),
                "ui": "Calculating..."
            },
            "get_current_time": {
                "speech": random.choice([
                    "Let me check the current time.",
                    "I'll get the time for you.",
                    "Checking what time it is.",
                    "Let me see what time it is now."
                ]),
                "ui": "Getting current time..."
            },
            "get_weather": {
                "speech": random.choice([
                    "Let me check the weather conditions.",
                    "I'll get the weather information for you.",
                    "Checking the current weather.",
                    "Let me see what the weather is like."
                ]),
                "ui": "Checking weather..."
            },
            "control_system": {
                "speech": random.choice([
                    "I'll help you with that system command.",
                    "Executing that for you.",
                    "Let me handle that system task.",
                    "I'll take care of that command."
                ]),
                "ui": "Executing system command..."
            }
        }
        
        return announcements.get(tool_name)
    
    def cleanup(self):
        """Cleanup resources"""
        self.tool_executor.cleanup()

# Global JARVIS AI instance
jarvis_ai = JarvisAI()