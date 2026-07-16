import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")
client = Groq(api_key=my_api_key)

model = "llama-3.3-70b-versatile"
role = "user"
Prompt1 = "Write a short poem about the beauty of mankind"
Prompt2 = "Write a short poem about the beauty of nature"
Prompt3 = "Write a short poem about the beauty of love"
prompts = [Prompt1, Prompt2, Prompt3]
for Prompt in prompts:
    message = [{"role": role, "content": Prompt}]
    response = client.chat.completions.create(
        model=model, messages=message, max_tokens=100
    )
    usage = response.usage
    print(f"Prompt: {Prompt}")
    print(f"Input Tokens: {usage.prompt_tokens}")
    print(f"Output Tokens: {usage.completion_tokens}")
    print(f"Total Tokens: {usage.total_tokens}")
    print(f"finish Reason: {response.choices[0].finish_reason}")
    print(
        "@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@--@"
    )
    print(response.choices[0].message.content)
