from openai import OpenAI
from dotenv import load_dotenv
import os
import httpx

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), http_client=httpx.Client())
try:
    response = client.models.list()
    print("API key valid. Available models:", [model.id for model in response.data])
except Exception as e:
    print("API key error:", str(e))