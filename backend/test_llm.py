from types import SimpleNamespace

import groq
import httpx
import llm
import pytest


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

# any other error should become a generic LLMError
@pytest.mark.anyio
async def test_other_error_becomes_llm_error(monkeypatch):
    async def fake_create(**kwargs):
        request = httpx.Request("POST", "https://api.groq.com")
        response = httpx.Response(500, request=request)
        raise groq.InternalServerError("server error", response=response, body=None)

    fake_client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=fake_create)))
    monkeypatch.setattr(llm, "get_client", lambda: fake_client)

    with pytest.raises(llm.LLMError):
        await llm.complete("hi")

# if the answer is cut off error
@pytest.mark.anyio
async def test_cut_off_answer_is_rejected(monkeypatch):
    async def fake_create(**kwargs):
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="A thief who"), finish_reason="length")],
            usage=SimpleNamespace(total_tokens=512),
        )

    fake_client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=fake_create)))
    monkeypatch.setattr(llm, "get_client", lambda: fake_client)

    with pytest.raises(llm.LLMError):
        await llm.complete("hi")

# if the answer is clean, it should be returned
@pytest.mark.anyio
async def test_returns_clean_text(monkeypatch):
    async def fake_create(**kwargs):
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="  A heist film.  "), finish_reason="stop")],
            usage=SimpleNamespace(total_tokens=100),
        )

    fake_client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=fake_create)))
    monkeypatch.setattr(llm, "get_client", lambda: fake_client)

    assert await llm.complete("hi") == "A heist film."