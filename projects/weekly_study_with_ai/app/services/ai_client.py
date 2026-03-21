from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)


def analyze_text(prompt:str) -> str:

    response = client.chat.completions.create(
        model = settings.openai_model,
        messages=[
            {
                "role": "system",
                "content":"You are professional study planning assistant."
            },
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content or ""