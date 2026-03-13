# 🎙️ Voice AI Company Credibility Agent

An intelligent voice-based conversational AI agent that reads and interprets a company's credibility JSON report, answering questions naturally through speech.

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
├── main.py                   # Entry point
├── requirements.txt          # Dependencies
├── .env                      # API key (not committed)
└── README.md                 # This file
```

### Technology Stack

| Component        | Technology                         |
|------------------|------------------------------------|
| Speech-to-Text   | faster-whisper (base model)        |
| Text-to-Speech   | pyttsx3                            |
| LLM              | deepseek/deepseek-r1:free (OpenRouter) |
| Framework        | LangChain (ChatOpenAI, LLMChain, ConversationBufferMemory, PromptTemplate) |
| Audio Recording  | sounddevice + scipy                |

## ⚙️ Installation

### Prerequisites
- Python 3.9 or higher
- A working microphone (optional — text mode available)
- OpenRouter API key (free tier works)

### Step 1: Clone/Navigate to Project
```bash
cd "Voice AI Agent"
```

### Step 2: Create Virtual Environment (optional but recommended)
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
Create/edit the `.env` file in the project root:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```
Get a free API key from [OpenRouter](https://openrouter.ai/).

## 🚀 How to Run

### Voice Mode (default — uses microphone)
```bash
python main.py
```

### Text Mode (no microphone needed)
```bash
python main.py --text
```

## 💬 Supported Question Types

### 1. Company Basics
- "What is the company name?"
- "What is the CIN number?"
- "When was the company incorporated?"
- "What is the company status?"
- "What industry does the company operate in?"
- "What type of company is this?"

### 2. Management & Directors
- "Who are the directors?"
- "How many directors does the company have?"
- "Tell me about the managing director"
- "Who are the former directors?"
- "What is the company secretary's name?"

### 3. Financial Information
- "What is the turnover slab?"
- "What is the company's constitution?"

### 4. GST & Compliance
- "What is the GSTIN?"
- "What is the GST status?"
- "When was GST registration done?"
- "Are there any compliance issues?"

### 5. Alerts & Risk
- "What alerts exist for this company?"
- "How many high severity alerts are there?"
- "Are there any severe alerts?"
- "Is this company in good standing?"
- "Tell me about the alert summary"

### 6. Contact Information
- "What are the phone numbers?"
- "What are the email addresses?"
- "What is the company address?"
- "What is the company website?"

### 7. Reviews & Ratings
- "What is the Google rating?"
- "What are the JustDial reviews?"
- "How is the company rated overall?"

### 8. Awards & Certificates
- "What awards has the company received?"
- "What certificates does the company have?"

### 9. Opening Hours
- "What are the opening hours?"
- "Is the company open on Sunday?"

### 10. Follow-up Questions
- "Tell me more about that"
- "What about the email addresses?"
- "And the former directors?"

## 📝 Sample Conversation Transcript

```
User: "What is the company name?"
Agent: "The company is HESTER BIOSCIENCES LIMITED."

User: "When was it incorporated?"
Agent: "The company was incorporated on 29th April, 1987."

User: "Who are the current directors?"
Agent: "The company has 12 current directors and officers. The key members include:
1. Rajiv Gandhi - Managing Director (DIN: 00438037)
2. Sanjiv Dinesh Gandhi - Director (DIN: 00024548)
3. Ravin Kanti Gandhi - Director (DIN: 00438361)
4. Bhupendra Vithaldas Gandhi - Director (DIN: 00437907)
5. Priya Rajiv Gandhi - Whole-Time Director (DIN: 06998979)
...and others including Anil Jain, Jatin Trivedi, and more."

User: "What is the GST status?"
Agent: "The GST registration is active. The GSTIN is 06AAACH2863B1Z2,
and the company's turnover slab is Rs. 500 Crore and above."

User: "Are there any compliance issues?"
Agent: "Based on the alert summary, there are 2 high severity alerts,
2 medium severity alerts, and 1 low severity alert.
There are no severe alerts. The management-related alerts show
some former directors with deactivated DINs."

User: "What is the company's Google rating?"
Agent: "The company has a Google rating of 4.8 out of 5, based on 4 ratings."

User: "What awards has the company received?"
Agent: "The company received 'The Best Animal Vaccine Company' award,
which was awarded by The New Economy in the UK in 2010."

User: "What certificates does the company hold?"
Agent: "The company holds two certificates:
1. WHO-GMP Certification (Quality Certification)
2. DSIR Registration (Research & Development Certification)"

User: "What is the company website?"
Agent: "The company website is http://www.hester.in/"

User: "Is the company open on Sunday?"
Agent: "No, the company is closed on Sundays. On weekdays and Saturdays,
the opening hours are 9 AM to 6 PM."

User: "Tell me about the PAN number"
Agent: "The company's PAN number is AAACH2863B."

User: "Who is the owner?"
Agent: "The owner listed in the report is Rajiv Dinesh Gandhi."

User: "What is the company's primary address?"
Agent: "The primary registered address is: Plot No.-97, Industrial Area,
Phase-1, Panchkula, Panchkula, Haryana, 134113.
The company has a total of 55 registered addresses across India."

User: "Are there any bank-related alerts?"
Agent: "No, all bank-related alerts are clear. There are no issues with
bank defaulting, bank auction, or wilful bank defaulting."

User: "exit"
Agent: "Thank you for using the Voice AI Agent. Goodbye!"
```

## ⚠️ Known Limitations

1. **Free LLM Model**: Uses DeepSeek R1 free tier via OpenRouter — may have rate limits and occasional slowness.
2. **Whisper Base Model**: The "base" Whisper model provides decent accuracy but may struggle with strong accents or noisy environments. Upgrade to "small" or "medium" for better accuracy.
3. **Audio Duration**: Default recording is 7 seconds. Longer questions may get cut off.
4. **Internet Required**: The LLM requires an active internet connection (OpenRouter API).
5. **No Real-Time Streaming**: Responses are generated fully before being spoken.
6. **Single JSON File**: Currently reads a single pre-loaded JSON report.

## 🔧 Configuration

All settings can be adjusted in `config/settings.py`:

| Setting           | Default                    | Description                    |
|-------------------|----------------------------|--------------------------------|
| MODEL_NAME        | deepseek/deepseek-r1:free  | OpenRouter model identifier    |
| WHISPER_MODEL     | base                       | Whisper model size             |
| RECORD_DURATION   | 7                          | Seconds to record audio        |
| TTS_RATE          | 175                        | Speech rate (words/min)        |
| TTS_VOLUME        | 0.9                        | Speaker volume (0.0-1.0)       |
| LLM_TEMPERATURE   | 0.3                        | LLM creativity (lower=factual) |

## 📄 Reflection

Building this Voice AI Agent was an interesting exercise in integrating multiple AI technologies into a cohesive pipeline. The most challenging aspect was designing the JSON data extraction strategy — the credibility report is deeply nested with 13,000+ lines, and rather than building brittle keyword-matching extraction functions, I chose to generate a comprehensive text summary at startup and inject it into the LLM's context. This approach is more robust and flexible, allowing the LLM to answer any question about the data naturally. Another challenge was handling the DeepSeek R1 model's tendency to include `<think>` tags in responses, which required regex cleanup. The LangChain ConversationBufferMemory worked well for maintaining context across follow-up questions. If I were to improve this further, I would add: (1) streaming responses for faster perceived latency, (2) a web UI for easier interaction, (3) support for multiple JSON reports, and (4) a "confidence score" for answers to flag when the agent is uncertain.
