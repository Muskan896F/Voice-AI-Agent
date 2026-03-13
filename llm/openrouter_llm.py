"""
OpenRouter LLM integration using LangChain ChatOpenAI.
Configures the DeepSeek R1 free model via OpenRouter API.
"""

import logging
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


def get_llm(api_key: str, base_url: str, model_name: str,
            temperature: float = 0.3) -> ChatOpenAI:
    """
    Create and return a LangChain ChatOpenAI instance configured
    to use OpenRouter's API with the specified model.
    
    Args:
        api_key: OpenRouter API key
        base_url: OpenRouter API base URL
        model_name: Model identifier (e.g., 'deepseek/deepseek-r1:free')
        temperature: Sampling temperature (lower = more factual)
    
    Returns:
        Configured ChatOpenAI instance
    """
    if not api_key:
        raise ValueError(
            "OpenRouter API key is missing. "
            "Please set OPENROUTER_API_KEY in your .env file."
        )
    
    llm = ChatOpenAI(
        openai_api_key=api_key,
        openai_api_base=base_url,
        model_name=model_name,
        temperature=temperature,
        max_tokens=1024,
        model_kwargs={
            "extra_headers": {
                "HTTP-Referer": "http://localhost",
                "X-Title": "Voice AI Company Agent"
            }
        }
    )
    
    logger.info(f"LLM initialized: {model_name} via {base_url}")
    return llm
