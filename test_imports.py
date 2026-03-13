import sys
sys.path.insert(0, '.')

from config.settings import OPENROUTER_API_KEY, JSON_DATA_PATH
print('Settings loaded OK')

from tools.json_tool import load_json, get_company_data_summary
data = load_json(JSON_DATA_PATH)
summary = get_company_data_summary(data)

print(f"Company: {data.get('name')}")
print(f"Summary length: {len(summary)} chars")

from llm.openrouter_llm import get_llm
from agent.credibility_agent import create_agent, ask_agent
from voice.text_to_speech import speak

print('ALL IMPORTS OK')
