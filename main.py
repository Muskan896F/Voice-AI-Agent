"""
Voice AI Agent - Main Entry Point
===================================
An intelligent voice-based conversational agent that answers questions
about a company's credibility by reading and analyzing a structured JSON report.

Technologies:
    - LangChain (LLMChain, ConversationBufferMemory, PromptTemplate)
    - OpenRouter API (deepseek/deepseek-r1:free)
    - faster-whisper (speech-to-text)
    - pyttsx3 (text-to-speech)

Usage:
    python main.py
    python main.py --text   (text-only mode, no microphone)
"""

import sys
import os
import logging
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import (
    OPENROUTER_API_KEY, OPENROUTER_BASE_URL, MODEL_NAME, LLM_TEMPERATURE,
    WHISPER_MODEL, WHISPER_DEVICE, WHISPER_COMPUTE_TYPE,
    SAMPLE_RATE, RECORD_DURATION, TEMP_AUDIO_FILE,
    TTS_RATE, TTS_VOLUME,
    JSON_DATA_PATH, LOG_FILE_PATH
)
from tools.json_tool import load_json, get_company_data_summary
from llm.openrouter_llm import get_llm
from agent.credibility_agent import create_agent, ask_agent
from voice.text_to_speech import speak


# ─── Logging Setup ──────────────────────────────────────────────────────
def setup_logging():
    """Configure logging to both file and console."""
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE_PATH, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def log_conversation(question: str, answer: str):
    """Log a conversation turn to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE_PATH, 'a', encoding='utf-8') as f:
        f.write(f"\n[{timestamp}]\n")
        f.write(f"USER: {question}\n")
        f.write(f"AGENT: {answer}\n")
        f.write("-" * 60 + "\n")


# ─── Input Handling ──────────────────────────────────────────────────────
def get_voice_input() -> str:
    """Get user input via voice (microphone + Whisper)."""
    from voice.speech_to_text import listen
    return listen(
        duration=RECORD_DURATION,
        sample_rate=SAMPLE_RATE,
        temp_file=TEMP_AUDIO_FILE,
        model_size=WHISPER_MODEL,
        device=WHISPER_DEVICE,
        compute_type=WHISPER_COMPUTE_TYPE
    )


def get_text_input() -> str:
    """Get user input via text (keyboard)."""
    return input("\n📝 You: ").strip()


# ─── Main Application ───────────────────────────────────────────────────
def main():
    """Main entry point for the Voice AI Agent."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Determine input mode
    text_mode = "--text" in sys.argv
    
    # ─── Banner ──────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("  🎙️  VOICE AI COMPANY CREDIBILITY AGENT  🎙️")
    print("=" * 65)
    print("  Powered by: LangChain + DeepSeek R1 + Whisper + pyttsx3")
    print("  Mode: " + ("TEXT INPUT" if text_mode else "VOICE INPUT (with text fallback)"))
    print("  Say 'exit', 'quit', or 'bye' to end the conversation.")
    print("=" * 65)
    
    # ─── 1. Load JSON Data ───────────────────────────────────────────
    print("\n⏳ Loading company credibility report...")
    try:
        json_data = load_json(JSON_DATA_PATH)
        company_name = json_data.get('name', 'Unknown Company')
        print(f"✅ Loaded report for: {company_name}")
    except Exception as e:
        print(f"❌ Failed to load JSON data: {e}")
        sys.exit(1)
    
    # ─── 2. Generate Data Summary ────────────────────────────────────
    print("⏳ Processing company data...")
    company_summary = get_company_data_summary(json_data)
    print(f"✅ Data summary prepared ({len(company_summary)} characters)")
    
    # ─── 3. Initialize LLM ──────────────────────────────────────────
    print("⏳ Connecting to LLM (OpenRouter - DeepSeek R1)...")
    try:
        llm = get_llm(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
            model_name=MODEL_NAME,
            temperature=LLM_TEMPERATURE
        )
        print("✅ LLM connected successfully")
    except Exception as e:
        print(f"❌ Failed to initialize LLM: {e}")
        sys.exit(1)
    
    # ─── 4. Create Agent ─────────────────────────────────────────────
    print("⏳ Setting up conversational agent...")
    chain, memory = create_agent(llm, company_summary)
    print("✅ Agent ready!\n")
    
    # ─── 5. Welcome Message ──────────────────────────────────────────
    welcome_msg = (
        f"Hello! I'm your AI assistant. I've analyzed the credibility report for "
        f"{company_name}. You can ask me anything about the company — "
        f"directors, GST status, alerts, financials, compliance, and more. "
        f"How can I help you?"
    )
    print(f"🤖 Agent: {welcome_msg}\n")
    speak(welcome_msg, rate=TTS_RATE, volume=TTS_VOLUME)
    
    # ─── 6. Conversation Loop ────────────────────────────────────────
    while True:
        try:
            # Get user input
            if text_mode:
                user_input = get_text_input()
            else:
                user_input = get_voice_input()
            
            # Check for empty input
            if not user_input:
                print("⚠️  I didn't catch that. Please try again.")
                continue
            
            # Check for exit commands
            if user_input.lower().strip() in ['exit', 'quit', 'bye', 'stop', 'end']:
                goodbye_msg = "Thank you for using the Voice AI Agent. Goodbye!"
                print(f"\n🤖 Agent: {goodbye_msg}")
                speak(goodbye_msg, rate=TTS_RATE, volume=TTS_VOLUME)
                log_conversation(user_input, goodbye_msg)
                break
            
            # Get agent response
            print("\n⏳ Thinking...")
            response = ask_agent(chain, memory, company_summary, user_input)
            
            # Display and speak response
            print(f"\n🤖 Agent: {response}\n")
            speak(response, rate=TTS_RATE, volume=TTS_VOLUME)
            
            # Log the conversation
            log_conversation(user_input, response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Session ended by user. Goodbye!")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            error_msg = "I encountered an unexpected error. Let me try again."
            print(f"\n🤖 Agent: {error_msg}")
            speak(error_msg, rate=TTS_RATE, volume=TTS_VOLUME)
    
    print("\n" + "=" * 65)
    print("  Session ended. Conversation log saved to:")
    print(f"  {LOG_FILE_PATH}")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
