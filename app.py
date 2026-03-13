import streamlit as st
import os
import sys
import logging
import threading
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
from voice.text_to_speech import speak, save_speech_to_file
from voice.speech_to_text import listen

# ─── Page Config ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Voice AI Credibility Agent",
    page_icon="🎙️",
    layout="wide"
)

# ─── Custom CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .user-message {
        background-color: #f0f2f6;
    }
    .agent-message {
        background-color: #e8f4f8;
    }
    .main {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# ─── Initialization ──────────────────────────────────────────────────────
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'agent' not in st.session_state:
    try:
        # Load data
        json_data = load_json(JSON_DATA_PATH)
        company_name = json_data.get('name', 'Unknown Company')
        company_summary = get_company_data_summary(json_data)
        
        # Initialize LLM
        llm = get_llm(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
            model_name=MODEL_NAME,
            temperature=LLM_TEMPERATURE
        )
        
        # Create Agent
        chain, memory = create_agent(llm, company_summary)
        
        st.session_state.agent = {
            'chain': chain,
            'memory': memory,
            'company_summary': company_summary,
            'company_name': company_name
        }
    except Exception as e:
        st.error(f"Failed to initialize agent: {e}")
        st.stop()

# ─── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🎙️ Voice AI Agent")
    st.info(f"Connected to: **{st.session_state.agent['company_name']}**")
    st.divider()
    
    st.subheader("Controls")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.agent['memory'] = []
        st.rerun()

    st.divider()
    st.write(f"**Model:** {MODEL_NAME}")
    st.write(f"**STT:** Whisper {WHISPER_MODEL}")

# ─── Chat Interface ─────────────────────────────────────────────────────
st.title("🛡️ Company Credibility Chatbot")

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ─── Input Area ────────────────────────────────────────────────────────
# Use separate columns for Voice and Text input
col1, col2 = st.columns([0.15, 0.85])

with col1:
    if st.button("🎤 Record"):
        with st.spinner("Listening..."):
            user_input = listen(
                duration=RECORD_DURATION,
                sample_rate=SAMPLE_RATE,
                temp_file=TEMP_AUDIO_FILE,
                model_size=WHISPER_MODEL,
                device=WHISPER_DEVICE,
                compute_type=WHISPER_COMPUTE_TYPE
            )
            
            if user_input:
                st.session_state.pending_voice_input = user_input
                st.rerun()
            else:
                st.warning("No speech detected.")

# Handle text input
if prompt := st.chat_input("Ask about company credibility..."):
    user_input = prompt
else:
    user_input = st.session_state.get('pending_voice_input', None)
    if user_input:
        del st.session_state.pending_voice_input

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate and display agent response
    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            response = ask_agent(
                st.session_state.agent['chain'],
                st.session_state.agent['memory'],
                st.session_state.agent['company_summary'],
                user_input
            )
            st.markdown(response)
            
            # Generate and play audio response
            audio_path = "agent_response.wav"
            if save_speech_to_file(response, audio_path, rate=TTS_RATE, volume=TTS_VOLUME):
                st.audio(audio_path, format="audio/wav", autoplay=True)
            else:
                st.warning("⚠️ Could not generate audio for this response.")
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# ─── Footer ────────────────────────────────────────────────────────────
st.divider()
st.caption(f"© {datetime.now().year} Voice AI Credibility Agent • Powered by OpenRouter & Whisper")
