







from model.provider import Provider


class Agent:
    def __init__(self, provider: Provider | None = None, model_name: str | None = None):
        self.provider = provider
        self.model_name = model_name

    def send(self,user_text:str,temperature: float = 0.7, max_tokens: int = 256, timeout: float = 180, tools: list[dict] | None = None):
        from model.client import chat


        messages = [{"role": "user", "content": user_text}]


        response = chat(
            model_name=self.model_name or self.provider.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            provider=self.provider,
            timeout=timeout,
            tools=tools
        )
        return response.content