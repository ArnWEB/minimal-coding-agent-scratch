from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

@dataclass
class Provider:
    model_name: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None

    @classmethod
    def from_env(cls) -> Provider:
        import os
        load_dotenv()
        return cls(
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL"),
            model_name=os.getenv("LLM_MODEL_NAME")
        )
    
def ollama():
    import os
    load_dotenv()
    return Provider(
        api_key=os.getenv("OLLAMA_API_KEY"),
        base_url=os.getenv("OLLAMA_BASE_URL"),
        model_name=os.getenv("OLLAMA_MODEL_NAME")
    )

def openai():
    import os
    load_dotenv()
    return Provider(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        model_name=os.getenv("OPENAI_MODEL_NAME")
    )
    