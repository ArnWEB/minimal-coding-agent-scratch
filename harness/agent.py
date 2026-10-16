
import os

from icecream import ic

from harness.context import deliver
from harness.workspace import Workspace
from model.provider import Provider


class Agent:
    def __init__(self, provider: Provider | None = None, model_name: str | None = None , history: list[dict] | None = [],workspace: str | None = None,stream: bool = False):
        self.provider = provider
        self.workspace = Workspace(root_path=workspace) if workspace else Workspace(os.getcwd())
        self.model_name = model_name
        self.history = history or []
        self.stream = stream
        ic(f"Agent initialized with provider: {self.provider}, model_name: {self.model_name}, history: {self.history}, workspace: {self.workspace.root_path}, stream: {self.stream}")

    def _read_agent_md(self):
        return self.workspace.read_file("agent.md")


    def send(self,user_text:str,temperature: float = 0.7, max_tokens: int = 256, timeout: float = 180, tools: list[dict] | None = None):
        from model.client import chat

        # ic(f"send called with user_text: {user_text}, temperature: {temperature}, max_tokens: {max_tokens}, timeout: {timeout}, tools: {tools}, stream: {self.stream}")


        system_message = [{"role": "system", "content": self._read_agent_md()}] if self._read_agent_md() else []



        current_messages = {"role": "user", "content": user_text}

        if self.stream==False:
            self.history.append(current_messages)

            response = chat(
                model_name=self.model_name or self.provider.model_name,
                messages=system_message + self.history,
                temperature=temperature,
                max_tokens=max_tokens,
                provider=self.provider,
                timeout=timeout,
                tools=tools,
                stream=self.stream,
            )
            # print(f"Response received: {response}")

            self.history.append({"role":"assistant", "content": response.content})
            return response.content
        # else:

        #     self.history.append(current_messages)

        #     for file_content in deliver(user_text):
        #         self.history.append({"role":"assistant", "content": f"File context: {file_content}"})

        #     streamed_content = []

        #     for response in chat(
        #         model_name=self.model_name or self.provider.model_name,
        #         messages= system_message + self.history,
        #         temperature=temperature,
        #         max_tokens=max_tokens,
        #         provider=self.provider,
        #         timeout=timeout,
        #         tools=tools,
        #         stream=self.stream,
        #     ):
        #         streamed_content.append(response.content)
        #         yield response.content

        #     # Streaming responses do not need a provider-specific "done" event.
        #     # The iterator's completion is the reliable boundary for history.
        #     self.history.append(
        #         {
        #             "role": "assistant",
        #             "content": "".join(streamed_content),
        #         }
        #     )


    def send_stream(self,user_text:str,temperature: float = 0.7, max_tokens: int = 256, timeout: float = 180, tools: list[dict] | None = None):
        from model.client import chat_stream

        # ic(f"send_stream called with user_text: {user_text}, temperature: {temperature}, max_tokens: {max_tokens}, timeout: {timeout}, tools: {tools}")

        system_message = [{"role": "system", "content": self._read_agent_md()}] if self._read_agent_md() else []

        current_messages = {"role": "user", "content": user_text}
        self.history.append(current_messages)

        for file_content in deliver(user_text):
            self.history.append({"role":"assistant", "content": f"File context: {file_content}"})

        streamed_content = []

        for response in chat_stream(
            model_name=self.model_name or self.provider.model_name,
            messages= system_message + self.history,
            temperature=temperature,
            max_tokens=max_tokens,
            provider=self.provider,
            timeout=timeout,
            tools=tools,
        ):
            streamed_content.append(response.content)
            yield response.content

        # Streaming responses do not need a provider-specific "done" event.
        # The iterator's completion is the reliable boundary for history.
        self.history.append(
            {
                "role": "assistant",
                "content": "".join(streamed_content),
            }
        )