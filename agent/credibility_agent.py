"""
Credibility Agent using LangChain Core.
Creates a conversational agent with manual memory that answers questions
about company credibility data using an LLM.
"""

import logging
import re
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

logger = logging.getLogger(__name__)

# System prompt with company data context
AGENT_SYSTEM_PROMPT = """You are an intelligent AI assistant that answers questions about a company's credibility report. You have access to the following company data:

--- COMPANY DATA START ---
{company_data}
--- COMPANY DATA END ---

INSTRUCTIONS:
1. Answer questions ONLY based on the company data provided above.
2. Give clear, concise, and conversational responses.
3. If the data for a question is not available in the report, say: "This information is not available in the report."
4. When mentioning numbers like capital amounts, convert them to user-friendly formats (e.g., "10 lakh rupees" instead of "1000000").
5. When listing directors, include their name, designation, and DIN.
6. For alerts, clearly state the severity and what the alert is about.
7. Do NOT make up information. Only use what is in the data above.
8. Keep responses brief and natural — you are a voice assistant, so responses should be spoken aloud.
9. Use Indian English conventions (e.g., "lakh", "crore").
10. If the user asks a follow-up question, use the conversation history for context.
"""


def create_agent(llm, company_data_summary: str):
    """
    Create an agent executor using modern LCEL syntax.
    
    Args:
        llm: The ChatOpenAI LLM instance
        company_data_summary: Text summary of the company data
    
    Returns:
        Tuple of (chain, memory_list)
    """
    # Create the prompt using ChatPromptTemplate
    prompt = ChatPromptTemplate.from_messages([
        ("system", AGENT_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    # Modern LCEL chain
    chain = prompt | llm
    
    # Manual memory list
    memory = []
    
    logger.info("Credibility agent created (LCEL) with manual memory")
    return chain, memory


def ask_agent(chain, memory: list, company_data_summary: str, question: str) -> str:
    """
    Send a question to the agent and get a response.
    
    Args:
        chain: The LCEL chain instance
        memory: List storing conversation history
        company_data_summary: Text summary of company data
        question: User's question
    
    Returns:
        Agent's response text
    """
    try:
        # Generate response using the chain
        response = chain.invoke({
            "company_data": company_data_summary,
            "history": memory,
            "input": question
        })
        
        answer = response.content.strip()
        
        # Clean up any <think>...</think> tags from DeepSeek R1
        answer = re.sub(r'<think>.*?</think>', '', answer, flags=re.DOTALL).strip()
        
        if not answer:
            answer = "I couldn't generate a response. Please try rephrasing your question."
        
        # Update memory (keep last 10 messages max to save context space)
        memory.append(HumanMessage(content=question))
        memory.append(AIMessage(content=answer))
        
        if len(memory) > 10:
            memory = memory[-10:]
            
        logger.info(f"Q: {question}")
        logger.info(f"A: {answer}")
        
        return answer
        
    except Exception as e:
        logger.error(f"Agent error: {e}")
        return f"I encountered an error while processing your question: {e}"
