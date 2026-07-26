from harness.agent import Agent
from model.provider import ollama


def main() -> None:

    provider = ollama()
    agent = Agent(provider=provider, model_name=provider.model_name)

    print("agent ready (ch-01) — stateless: every turn is an independent model call,")
    print("so it can't remember anything yet (watch it forget). Ctrl-D to exit.")
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