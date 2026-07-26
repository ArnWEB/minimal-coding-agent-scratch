


from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LLMResponse:
    content: str
    reasoning_text: str
    finish_reason: str
    raw: dict = field(default_factory=dict)
    tools: list =field(default_factory=list)
    usage: dict = field(default_factory=dict)



