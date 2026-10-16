import re
from pathlib import Path


def deliver(user_input: str) -> list[str]:
    file_paths = re.findall(r"@(\S+)", user_input)
    results: list[str] = []
    for path in file_paths:
        p = Path(path).resolve()
        if p.is_file():
            results.append(p.read_text())
        else:
            results.append(f"File '{path}' does not exist.")
    return results