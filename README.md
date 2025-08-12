# JARVIS-AI

A personal AI assistant project that uses voice recognition, face authentication, and various smart features to help automate tasks.

---

## Features

- Face Authentication for secure access
- Voice commands for hands-free interaction
- **Persistent Chat History** - All conversations are saved and can be viewed anytime
- Open applications and websites
- Send WhatsApp messages, make calls, and video calls
- Play YouTube videos
- Chatbot integration for general queries
- Text-to-speech responses

---

## Chat History & Context

The AI assistant now includes persistent chat history with contextual awareness:

### **Chat History Features:**
- **View History**: Click the chat icon (💬) to view all previous conversations
- **Auto-Save**: All user messages and AI responses are automatically saved to the database
- **Timestamps**: Each conversation includes date and time information
- **Clear History**: Option to clear all chat history when needed
- **Refresh**: Real-time updates when viewing chat history

### **Contextual AI Responses:**
- **Memory**: AI remembers previous conversations and can reference them
- **Continuity**: Conversations flow naturally with context from recent interactions
- **Personalization**: AI can remember your preferences, name, and previous topics
- **Smart Context**: Uses last 5 conversations as context (configurable)

### **Configuration:**
- **Context Limit**: Adjust how many previous conversations to include (default: 5)
- **Toggle Context**: Enable/disable contextual responses in `backend/openai_config.py`
- **Storage**: Chat history is stored in SQLite database (`jarvis.db`) and persists between sessions

**Example:** If you tell JARVIS "My name is John" in one conversation, it will remember your name in future conversations!

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/raziquehasan/JARVIS-AI.git
   cd JARVIS-AI
Create and activate a Python virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate       # Windows
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Usage
Run the main script:

bash
Copy
Edit
python main.py
Follow on-screen instructions for face authentication and voice commands.

Dependencies
Python 3.x

pyttsx3

SpeechRecognition

eel

Other dependencies as listed in requirements.txt

Contribution
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
Razique Hasan 
