from langchain_google_genai import ChatGoogleGenerativeAI
import os

class BaseLLM:
    def __init__(self):
        api_key=os.getenv("GOOGLE_API_KEY")
        self.basellm=ChatGoogleGenerativeAI(model='gemini-1.5-flash',api_key=api_key)
