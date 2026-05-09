import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHAT_ID = os.getenv("CHAT_ID")
