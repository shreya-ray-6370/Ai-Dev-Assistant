from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama3-groq-70b-8192-tool-use-preview",
    api_key=os.environ["GROQ_API_KEY"]
)