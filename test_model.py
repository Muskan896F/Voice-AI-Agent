import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load env
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

print(f"Testing with API Key: {api_key[:10]}...")

try:
    llm = ChatOpenAI(
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        model_name="openrouter/free",
        temperature=0.7,
        default_headers={
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "Voice AI Agent Test"
        }
    )

    print("Sending test message...")
    response = llm.invoke([HumanMessage(content="Hello, are you active? Answer in 5 words.")])
    print(f"Response: {response.content}")
    print("SUCCESS: Model is active and valid!")

except Exception as e:
    print(f"FAILED: {e}")
