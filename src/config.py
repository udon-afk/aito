import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    print("Error: DISCORD_TOKEN is not set in .env")
    
CHAT_CHANNEL_ID = int(os.getenv("CHAT_CHANNEL_ID", 0))
SCORE_CHANNEL_ID = int(os.getenv("SCORE_CHANNEL_ID", 0))
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID", 0))
BOT_USER_ID = os.getenv("BOT_USER_ID")
if BOT_USER_ID:
    BOT_USER_ID = int(BOT_USER_ID)

# Services
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "medium")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
SBV2_URL = os.getenv("SBV2_URL", "http://127.0.0.1:5000")

# Vector DB
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/memory")

# Websocket / API
WS_HOST = "0.0.0.0"
WS_PORT = 8000
