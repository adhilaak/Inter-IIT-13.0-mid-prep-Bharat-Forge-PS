from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

class AgentLLM:
    def __init__(self):
        self.basellm=ChatGoogleGenerativeAI(model="gemini-1.5-flash",api_key=os.getenv("GOOGLE_API_KEY"))
