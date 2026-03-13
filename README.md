# 🎙️ Voice AI Company Credibility Agent

An intelligent voice-based conversational AI agent that reads and interprets a company's credibility JSON report, answering questions naturally through speech. The agent is powered by LangChain, DeepSeek R1, and Whisper, offering both a modern web interface and a flexible command-line interface.

## 🏗️ Architecture

```
Voice AI Agent/
├── config/
│   └── settings.py          # Configuration & environment variables
├── voice/
│   ├── speech_to_text.py     # Microphone recording + Whisper STT
│   └── text_to_speech.py     # pyttsx3 TTS engine
├── tools/
│   └── json_tool.py          # JSON data loading & summary extraction
├── llm/
│   └── openrouter_llm.py     # OpenRouter LLM setup (DeepSeek R1)
├── agent/
│   └── credibility_agent.py  # LangChain conversational agent + memory
├── logs/
│   └── conversation.log      # Auto-generated conversation logs
├── Data/
│   └── company_credibility_report.json  # Input data
├── app.py                   # Streamlit Web Application (Modern UI)
├── main.py                   # CLI Entry point (Voice/Text mode)
├── requirements.txt          # Dependencies
├── .env                      # API key (not committed)
└── README.md                 # This file
```

### Technology Stack

| Component        | Technology                         |
|------------------|------------------------------------|
| **Web UI**       | Streamlit 🚀                       |
| **Speech-to-Text**| faster-whisper (base model)        |
| **Text-to-Speech**| pyttsx3                            |
| **LLM**          | deepseek/deepseek-r1:free (OpenRouter) |
| **Framework**    | LangChain                          |
| **Audio**        | sounddevice + scipy                |

## ⚙️ Installation

### Prerequisites
- Python 3.9 or higher
- A working microphone (optional — text mode available)
- OpenRouter API key

### Step 1: Clone/Navigate to Project
```bash
git clone https://github.com/Muskan896F/Voice-AI-Agent.git
cd "Voice AI Agent"
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up API Key
Create a `.env` file in the project root:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## 🚀 How to Run

### Option 1: Web Interface (Recommended)
Enjoy a modern ChatGPT-like interface with instant audio playback and chat history.
```bash
streamlit run app.py
```

### Option 2: CLI - Voice Mode
```bash
python main.py
```

### Option 3: CLI - Text Mode (No Mic Needed)
```bash
python main.py --text
```

## 💬 Supported Question Types

The agent can answer any question based on the provided JSON report, including:
- **Company Basics**: Name, CIN, Status, Industry.
- **Management**: Directors, Secretary, Former Directors.
- **Compliance**: GST status, Risk alerts, Financial turnover.
- **Contact**: Address, Website, Phone, Email.
- **Ratings**: Google ratings, JustDial reviews, Awards.

## 📝 Sample Conversation

> **User**: "What is the company's GST status?"
> **Agent**: "The GST registration is active. The GSTIN is 06AAACH2863B1Z2, and the company's turnover slab is Rs. 500 Crore and above."

## ⚠️ Known Limitations

1. **Free LLM Model**: Uses DeepSeek R1 free tier — may have rate limits.
2. **Whisper Base Model**: Decent accuracy, but may struggle in noisy environments.
3. **Internet Required**: Required for LLM (OpenRouter API).

## 🔧 Configuration

Adjust settings in `config/settings.py`:
- `RECORD_DURATION`: Seconds to record audio (Default: 7s).
- `TTS_RATE`: Speech speed.
- `WHISPER_MODEL`: Change from 'base' to 'small' for better accuracy.

---
Created by [Muskan](https://github.com/Muskan896F)
