import os
import pathlib
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel


class Ticket(BaseModel):
    name: str
    email: str
    issue: str
    phone_number: str


schema = Ticket.model_json_schema()

response_format = {"type": "json_object"}

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set")

client = Groq(api_key=my_api_key)

model = "llama-3.3-70b-versatile"

role = "user"

text = "Hello, my name is pranjal. I purchased an AC from you your company and its not working properly. I want to return it and get a refund. Can you help me with that? I am giving you the details of the product and the order number. The product is a LG AC model number LG12345 and the order number is 987654321. I have attached the invoice and the warranty card as well. Please let me know what are the steps to return the product and get a refund.you can contact me on my email which is pranjal@example.com or my phone number 123-456-7890. Thank you."


prompt = f"This is an issuse raised by a customer. please exatract the personal information from the {text} and return it in a json output based on this {schema}. "

message = [{"role": role, "content": prompt}]

response = client.chat.completions.create(
    model=model, messages=message, response_format=response_format
)

json_text = response.choices[0].message.content

ticket = Ticket.model_validate_json(json_text)

print(ticket)
