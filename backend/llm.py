import os
from groq import AsyncGroq

client = AsyncGroq(api_key=os.environ["GROQ_API_KEY"])


async def complete(prompt: str) -> str:
    response = await client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content