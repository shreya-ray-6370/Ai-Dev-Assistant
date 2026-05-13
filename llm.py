from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # ~6x higher free TPM than openai/gpt-oss-120b
    api_key=os.environ["GROQ_API_KEY"]
)


# Vision LLM — for image analysis and UI code generation
vision_llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=os.environ["GROQ_API_KEY"]
)