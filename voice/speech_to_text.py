"""
Speech-to-Text module using faster-whisper.
Records audio from microphone and transcribes it to text.
Falls back to text input if microphone is unavailable.
"""

import os
import sys
import numpy as np
import logging

logger = logging.getLogger(__name__)


def record_audio(duration: int, sample_rate: int, temp_file: str) -> str:
    """
    Record audio from the microphone and save as a WAV file.
    
    Args:
        duration: Recording duration in seconds
        sample_rate: Audio sample rate (16000 for Whisper)
        temp_file: Path to save the temporary WAV file
    
    Returns:
        Path to the saved audio file
    
    Raises:
        RuntimeError: If microphone recording fails
    """
    try:
        import sounddevice as sd
        from scipy.io.wavfile import write as wav_write

        print(f"\n🎤 Listening... (speak for {duration} seconds)")
        
        # Record audio from default microphone
        audio_data = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype='int16'
        )
        sd.wait()  # Wait until recording is finished
        
        # Save as WAV file
        wav_write(temp_file, sample_rate, audio_data)
        logger.info(f"Audio recorded and saved to {temp_file}")
        
        return temp_file
        
    except Exception as e:
        logger.error(f"Microphone recording failed: {e}")
        raise RuntimeError(f"Could not record audio: {e}")


def transcribe_audio(audio_file: str, model_size: str = "base",
                     device: str = "cpu", compute_type: str = "int8") -> str:
    """
    Transcribe audio file to text using faster-whisper.
    
    Args:
        audio_file: Path to the audio file
        model_size: Whisper model size (tiny, base, small, medium, large)
        device: Device to run inference on (cpu or cuda)
        compute_type: Computation type (int8, float16, float32)
    
    Returns:
        Transcribed text string
    """
    from faster_whisper import WhisperModel
    
    logger.info(f"Loading Whisper model: {model_size}")
    model = WhisperModel(model_size, device=device, compute_type=compute_type)
    
    logger.info(f"Transcribing audio: {audio_file}")
    segments, info = model.transcribe(audio_file, beam_size=5)
    
    # Combine all segments into one text
    transcribed_text = " ".join([segment.text.strip() for segment in segments])
    
    logger.info(f"Transcription result: {transcribed_text}")
    return transcribed_text


def listen(duration: int, sample_rate: int, temp_file: str,
           model_size: str = "base", device: str = "cpu",
           compute_type: str = "int8") -> str:
    """
    Full pipeline: record audio → transcribe → return text.
    Falls back to text input if recording fails.
    
    Args:
        duration: Recording duration in seconds
        sample_rate: Audio sample rate
        temp_file: Temporary audio file path
        model_size: Whisper model size
        device: Inference device
        compute_type: Computation type
    
    Returns:
        User's question as text (from speech or typed fallback)
    """
    try:
        # Record audio
        audio_path = record_audio(duration, sample_rate, temp_file)
        
        # Transcribe
        text = transcribe_audio(audio_path, model_size, device, compute_type)
        
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        if text.strip():
            print(f"📝 You said: {text}")
            return text.strip()
        else:
            print("⚠️  Could not understand the audio. Please type your question:")
            return input("You (text): ").strip()
            
    except RuntimeError:
        print("⚠️  Microphone not available. Switching to text input.")
        return input("You (text): ").strip()
    except Exception as e:
        logger.error(f"Speech-to-text error: {e}")
        print(f"⚠️  Speech recognition error. Please type your question:")
        return input("You (text): ").strip()
