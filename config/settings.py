"""
Configuration settings for the Voice AI Agent.
Loads environment variables and provides centralized configuration.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ─── OpenRouter LLM Settings ───────────────────────────────────────────
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "openrouter/free"
LLM_TEMPERATURE = 0.3

# ─── Whisper STT Settings ──────────────────────────────────────────────
WHISPER_MODEL = "base"
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8"

# ─── Audio Recording Settings ──────────────────────────────────────────
SAMPLE_RATE = 16000        # 16kHz for Whisper
RECORD_DURATION = 7        # seconds per recording
TEMP_AUDIO_FILE = "temp_audio.wav"

# ─── pyttsx3 TTS Settings ──────────────────────────────────────────────
TTS_RATE = 175             # words per minute
TTS_VOLUME = 0.9           # 0.0 to 1.0

# ─── File Paths ─────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_DATA_PATH = os.path.join(BASE_DIR, "Data", "company_credibility_report.json")
LOG_FILE_PATH = os.path.join(BASE_DIR, "logs", "conversation.log")
