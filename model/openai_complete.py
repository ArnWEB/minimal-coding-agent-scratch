import json

import httpx
from icecream import ic

from model.llm_response import LLMResponse
from model.provider import Provider


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
            "max_completion_tokens": max_tokens,
            "temperature": temperature,
            "tools": tools,
            "reasoning_effort": "medium",
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


## implement the streaming version of this
def get_openai_completion_stream(
    messages: list[dict],
    provider: Provider,
    max_tokens: int,
    temperature: float,
    tools: list[dict] | None,
    model: str | None,
    timeout: float = 180,
):
    base_url = provider.base_url.rstrip("/")
    model = model or provider.model
    api_key = provider.api_key
    ic(api_key)

    tools = tools if tools is not None else []

    with httpx.stream(
        "POST",
        url=f"{base_url}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": model,
            "messages": messages,
            "max_completion_tokens": max_tokens,
            "temperature": temperature,
            "tools": tools,
            "reasoning_effort": "medium",
            "stream": True,
        },
        timeout=timeout,
    ) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            # print(f"Received line: {line}")  # Debugging output
            if line.startswith("data: "):
                payload = line.removeprefix("data: ").strip() 
                try:
                    data = json.loads(payload)
                    choice = data.get("choices", [{}])[0]
                    delta = choice.get("delta", {})
                    yield LLMResponse(
                        content=delta.get("content", ""),
                        reasoning_text=delta.get("reasoning", ""),
                        finish_reason=choice.get("finish_reason", ""),
                        raw=data,
                        tools=delta.get("tools", []),
                        usage=data.get("usage", {}),
                    )
                except json.JSONDecodeError:
                    # print(f"Failed to decode JSON: {payload}")
                    pass
            

