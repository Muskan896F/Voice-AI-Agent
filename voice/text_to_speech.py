"""
Text-to-Speech module using pyttsx3.
Converts agent text responses into spoken audio output.
"""

import pyttsx3
import logging

logger = logging.getLogger(__name__)

# Global engine instance (initialized once)
_engine = None


def _get_engine(rate: int = 175, volume: float = 0.9) -> pyttsx3.Engine:
    """
    Get or create the pyttsx3 engine singleton.
    
    Args:
        rate: Speech rate in words per minute
        volume: Volume level (0.0 to 1.0)
    
    Returns:
        Configured pyttsx3 Engine instance
    """
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty('rate', rate)
        _engine.setProperty('volume', volume)
        
        # Try to use a natural-sounding voice
        voices = _engine.getProperty('voices')
        if voices:
            # Prefer a female English voice if available, else use default
            for voice in voices:
                if 'english' in voice.name.lower() or 'zira' in voice.name.lower():
                    _engine.setProperty('voice', voice.id)
                    break
        
        logger.info(f"TTS engine initialized (rate={rate}, volume={volume})")
    
    return _engine


def speak(text: str, rate: int = 200, volume: float = 1.0):
    """
    Convert text to speech and play it immediately (CLI mode).
    """
    try:
        engine = _get_engine()
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume)
        
        # Clean text for better speech
        text = text.replace('*', '').replace('_', '').strip()
        
        logger.info(f"Speaking: {text[:50]}...")
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        logger.error(f"TTS Error: {e}")


def save_speech_to_file(text: str, file_path: str, rate: int = 200, volume: float = 1.0):
    """
    Convert text to speech and save it to a file (Web/Streamlit mode).
    """
    try:
        # Use a fresh engine instance for file saving to avoid thread issues
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume)
        
        # Clean text
        text = text.replace('*', '').replace('_', '').strip()
        
        logger.info(f"Saving speech to {file_path}")
        engine.save_to_file(text, file_path)
        engine.runAndWait()
        return True
    except Exception as e:
        logger.error(f"Error saving speech to file: {e}")
        return False
        print(f"🔇 (Could not speak the response: {e})")
