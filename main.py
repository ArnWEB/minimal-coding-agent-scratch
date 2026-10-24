from uuid import uuid4

from icecream import ic

from harness.agent import Agent
from harness.tools import ToolRegistry, default_tools
from harness.workspace import Workspace,edit_file_tool,write_file_tool
from model.provider import openai

ic.disable()


def main() -> None:
    stream=False
    provider = openai()
    workspace= Workspace()
    tools = default_tools()
    tools.register(edit_file_tool(workspace))
    tools.register(write_file_tool(workspace))

    agent = Agent(provider=provider, model_name=provider.model_name,stream=stream)

    session_id = uuid4()
    print(f"Welcome to the Minimal Coding Agent Scratch! Your session id is {session_id}. Type your message below (Ctrl+D to exit):")

    if stream:
        while True:
            try:
                user = input("you> ")
            except EOFError:
                print()
                break
            if not user.strip():
                continue
            print("bot>", end=" ", flush=True)
            for response in agent.send_stream(user,max_tokens=1024,temperature=0.7,timeout=180):
                print(response, end="", flush=True)
            print()  # Print a newline after the bot's response
    else:
        while True:
            try:
                user = input("you> ")
            except EOFError:
                print()
                break
            if not user.strip():
                continue
            print("bot>", agent.send(user,max_tokens=1024,temperature=0.7,timeout=180))


if __name__ == "__main__":
    main()