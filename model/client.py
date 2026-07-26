from model.llm_response import LLMResponse
from model.provider import Provider
from model.openai_complete import get_openai_completion


def chat(
    model_name: str,
    messages: list[dict],
    temperature: float = 0.7,
    max_tokens: int = 1024,
    provider: Provider | None = None,
    timeout: float = 180,
    tools: list[dict] | None = None,
) -> LLMResponse:

    if provider is None:
        provider = Provider.from_env()

    if provider.model_name != model_name:
        raise ValueError(
            f"Provider model name '{provider.model_name}' does not match the requested model name '{model_name}'."
        )

    return get_openai_completion(
        messages=messages,
        provider=provider,
        max_tokens=max_tokens,
        temperature=temperature,
        tools=tools,
        model=model_name,
        timeout=timeout,
    )
