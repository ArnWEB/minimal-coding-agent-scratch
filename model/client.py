from collections.abc import Generator

from model.llm_response import LLMResponse
from model.openai_complete import get_openai_completion, get_openai_completion_stream
from model.provider import Provider


def chat(
    model_name: str,
    messages: list[dict],
    temperature: float = 0.7,
    max_tokens: int = 1024,
    provider: Provider | None = None,
    timeout: float = 180,
    tools: list[dict] | None = None,
    stream: bool = False,
):

    # print(f"chat called with model_name: {model_name}, messages: {messages}, temperature: {temperature}, max_tokens: {max_tokens}, provider: {provider}, timeout: {timeout}, tools: {tools}, stream: {stream}")

    if provider is None:
        provider = Provider.from_env()

    if provider.model_name != model_name:
        raise ValueError(
            f"Provider model name '{provider.model_name}' does not match the requested model name '{model_name}'."
        )
    # if stream:
    #     yield from get_openai_completion_stream(
    #         messages=messages,
    #         provider=provider,
    #         max_tokens=max_tokens,
    #         temperature=temperature,
    #         tools=tools,
    #         model=model_name,
    #         timeout=timeout,
    #     )

    return get_openai_completion(
        messages=messages,
        provider=provider,
        max_tokens=max_tokens,
        temperature=temperature,
        tools=tools,
        model=model_name,
        timeout=timeout,
    )

def chat_stream(
    model_name: str,
    messages: list[dict],
    temperature: float = 0.7,
    max_tokens: int = 1024,
    provider: Provider | None = None,
    timeout: float = 180,
    tools: list[dict] | None = None,
) -> Generator[LLMResponse]:

    # print(f"chat_stream called with model_name: {model_name}, messages: {messages}, temperature: {temperature}, max_tokens: {max_tokens}, provider: {provider}, timeout: {timeout}, tools: {tools}")

    if provider is None:
        provider = Provider.from_env()

    if provider.model_name != model_name:
        raise ValueError(
            f"Provider model name '{provider.model_name}' does not match the requested model name '{model_name}'."
        )

    yield from get_openai_completion_stream(
        messages=messages,
        provider=provider,
        max_tokens=max_tokens,
        temperature=temperature,
        tools=tools,
        model=model_name,
        timeout=timeout,
    )
