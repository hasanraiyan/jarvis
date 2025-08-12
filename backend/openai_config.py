import os

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', "dnasdhhsk")
OPENAI_API_BASE = os.getenv('OPENAI_API_BASE', 'https://text.pollinations.ai/openai')  # Default OpenAI API base URL
DEFAULT_MODEL = "openai"  # Changed back to standard OpenAI model
MAX_TOKENS = 150
TEMPERATURE = 0.7

# System message to define JARVIS's personality
SYSTEM_MESSAGE = "You are a helpful AI assistant named JARVIS."
