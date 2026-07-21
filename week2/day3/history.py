import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLM:

    def __init__(
        self,
        provider: str,
        model: str,
        api_key: str,
    ) -> None:

        self.provider = provider
        self.model = model

        if provider.lower() == "groq":
            self.client = Groq(api_key=api_key)

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def generate(
        self,
        messages: list[dict],
    ) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return response.choices[0].message.content

    def stream(
        self,
        messages: list[dict],
    ):

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
        )

        for chunk in stream:

            content = chunk.choices[0].delta.content

            if content:
                yield content


class ChatSession:

    def __init__(
        self,
        llm: LLM,
    ):

        self.llm = llm

        self.messages = []

    def send(
        self,
        prompt: str,
    ) -> str:

        self.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        reply = self.llm.generate(self.messages)

        self.messages.append(
            {
                "role": "assistant",
                "content": reply,
            }
        )

        return reply

    def stream(
        self,
        prompt: str,
    ):

        self.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        full_reply = ""

        for token in self.llm.stream(
            self.messages,
        ):

            full_reply += token

            yield token

        self.messages.append(
            {
                "role": "assistant",
                "content": full_reply,
            }
        )


api_key = os.getenv("GROQ_API_KEY")

llm = LLM(
    provider="groq",
    model="llama-3.3-70b-versatile",
    api_key=api_key,
)

chat = ChatSession(llm)

print(chat.send("Hello"))

print(chat.send("My name is Pranjal."))

print(chat.send("What's my name?"))
