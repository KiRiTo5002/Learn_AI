from dotenv import load_dotenv
from groq import Groq
import os


load_dotenv()


class LLM:
    """
    A reusable interface for interacting with an LLM provider.
    """

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
            raise ValueError(
                f"Unsupported provider: {provider}"
            )

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return response.choices[0].message.content


api_key = os.getenv("GROQ_API_KEY")

llm = LLM(
    provider="groq",
    model="llama-3.3-70b-versatile",
    api_key=api_key,
)

response = llm.generate(
    prompt="Explain Python in one sentence.",
)

print(response)