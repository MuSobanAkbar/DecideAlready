import os

from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv() 

client = AsyncGroq(
    
    api_key=os.environ["GROQ_API_KEY"],
    timeout=10,
    max_retries=1,
    )


async def complete(prompt: str) -> str:
    response = await client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content