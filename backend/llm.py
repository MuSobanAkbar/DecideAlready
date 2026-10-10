import os
from functools import lru_cache

import groq
from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv() 

@lru_cache(maxsize=1)
def get_client() -> AsyncGroq:
    return AsyncGroq(
        api_key=os.environ["GROQ_API_KEY"],
        timeout=10,
        max_retries=1,
    )

class LLMError(Exception):
    """The AI couldn't give us an answer."""


class LLMTimeout(LLMError):
    """The AI took too long."""


class LLMRateLimited(LLMError):
    """We've used up our free requests for now..."""



async def complete(prompt: str) -> str:
    try:
        response = await get_client().chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
        )
    except groq.APITimeoutError as e:
        raise LLMTimeout("Groq took too long to answer") from e
    except groq.RateLimitError as e:
        raise LLMRateLimited("Groq rate limit reached") from e
    except groq.APIError as e:
        raise LLMError(f"Groq error: {e}") from e


    choice = response.choices[0]
    text = (choice.message.content or "").strip()
    #  this is from groq doc and it is a signal for if the model ran out of room
    if choice.finish_reason == "length" or not text:
        raise LLMError("Groq returned an empty or cut-off answer")

    return text