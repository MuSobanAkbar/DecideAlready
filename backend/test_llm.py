from types import SimpleNamespace

import groq
import httpx
import pytest

import llm

# time out test
@pytest.mark.anyio
async def test_timeout_becomes_llm_timeout(monkeypatch):
    async def fake_create(**kwargs):
        raise groq.APITimeoutError(request=httpx.Request("POST", "https://api.groq.com"))

    fake_client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=fake_create)))
    monkeypatch.setattr(llm, "get_client", lambda: fake_client)

    with pytest.raises(llm.LLMTimeout):
        await llm.complete("hi")


# rate limit test 
@pytest.mark.anyio
async def test_rate_limit_becomes_llm_rate_limited(monkeypatch):
    async def fake_create(**kwargs):
        request = httpx.Request("POST", "https://api.groq.com")
        response = httpx.Response(429, request=request)
        raise groq.RateLimitError("rate limited", response=response, body=None)

    fake_client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=fake_create)))
    monkeypatch.setattr(llm, "get_client", lambda: fake_client)

    with pytest.raises(llm.LLMRateLimited):
        await llm.complete("hi")