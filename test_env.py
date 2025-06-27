from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("OPENAI_API_KEY:", api_key[:8] + "..." + api_key[-4:])  # Masked for security
else:
    print("ERROR: OPENAI_API_KEY not found")