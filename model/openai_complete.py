from model.llm_response import LLMResponse
from model.provider import Provider
import httpx
from icecream import ic


def get_openai_completion(
    messages: list[dict],
    provider: Provider,
    max_tokens: int,
    temperature: float,
    tools: list[dict] | None,
    model: str | None,
    timeout: float = 180,
) -> LLMResponse:

    base_url = provider.base_url.rstrip("/")
    model = model or provider.model
    api_key = provider.api_key
    ic(api_key)

    tools = tools if tools is not None else []

    response = httpx.post(
        url=f"{base_url}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": model,
            "messages": messages,
            "timeout": timeout,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "tools": tools,
        },
        timeout=timeout,
    )

    response.raise_for_status()

    raw_data = response.json()

    ic(raw_data)

    choice = raw_data.get("choices", [{}])[0]
    msg = choice.get("message", {})

    return LLMResponse(
        content=msg.get("content", ""),
        reasoning_text=msg.get("reasoning_text", ""),
        finish_reason=choice.get("finish_reason", ""),
        raw=raw_data,
        tools=msg.get("tools", []),
        usage=raw_data.get("usage", {}),
    )
