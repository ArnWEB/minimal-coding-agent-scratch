import ast
import operator
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}


def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression safely (no eval, just numbers + + - * / % **)."""

    def ev(node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _BINOPS:
            return _BINOPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -ev(node.operand)
        raise ValueError("unsupported expression")

    result = ev(ast.parse(expression, mode="eval").body)
    return str(int(result) if result == int(result) else result)


def read_file(path: str) -> str:
    """Return a file's contents, or an error string."""
    p = Path(path)
    return p.read_text() if p.is_file() else f"error: no such file: {path}"


@dataclass
class Tool:
    name: str
    description: str
    func: Callable[..., Any]
    parameters: dict[str, Any]


class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, Tool] = {}

    def register_tool(self, tool: Tool):
        if tool.name in self.tools:
            raise ValueError(f"Tool with name '{tool.name}' is already registered.")
        self.tools[tool.name] = tool


    def specs(self) -> dict[str, dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                },
            }
            for tool in self.tools.values()
        ]
    def call_tool(self, name: str, *args, **kwargs) -> Any:
        if name not in self.tools:
            raise ValueError(f"Tool with name '{name}' is not registered.")
        tool = self.tools[name]
        return tool.func(*args, **kwargs)

def default_tools() -> ToolRegistry:
    reg = ToolRegistry()
    reg.register(
        Tool(
            name="calculator",
            description="Evaluate an arithmetic expression like '47 * 89'.",
            parameters={
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
            func=calculator,
        )
    )
    reg.register(
        Tool(
            name="read_file",
            description="Read a UTF-8 text file from disk and return its contents.",
            parameters={
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
            func=read_file,
        )
    )
    return reg
