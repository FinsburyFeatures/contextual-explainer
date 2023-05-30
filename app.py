import os

import anthropic
from dotenv import load_dotenv

load_dotenv()

anthropic_client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))

print(anthropic_client)
print("hello world")
