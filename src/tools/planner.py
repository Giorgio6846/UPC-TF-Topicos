from langsmith import Client
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
from os import getenv

client = Client(api_key=getenv("LANGSMITH_API_KEY"))
model = ChatGoogleGenerativeAI(model="gemini-2.0")
prompt = client.pull_prompt("deepresearch", include_model=True)
print(prompt)