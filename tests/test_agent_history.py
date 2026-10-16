import unittest
from unittest.mock import patch

from harness.agent import Agent
from model.llm_response import LLMResponse
from model.provider import Provider


class AgentHistoryTests(unittest.TestCase):
    def test_streaming_history_is_appended_after_stream_finishes(self):
        provider = Provider(model_name="openai/gpt-oss-120b", api_key="test")
        agent = Agent(provider=provider, model_name=provider.model_name, stream=True)

        chunks = [
            LLMResponse(content="Hello", reasoning_text="", finish_reason=None),
            LLMResponse(content=" world", reasoning_text="", finish_reason=None),
        ]

        with patch("model.client.chat", return_value=iter(chunks)):
            output = list(agent.send("Hi"))

        self.assertEqual(output, ["Hello", " world"])
        self.assertEqual(
            agent.history,
            [
                {"role": "user", "content": "Hi"},
                {"role": "assistant", "content": "Hello world"},
            ],
        )


if __name__ == "__main__":
    unittest.main()
