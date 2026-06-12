from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        groq_api_key=os.getenv("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")
    )