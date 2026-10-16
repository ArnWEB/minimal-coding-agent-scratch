import os
import tempfile
from pathlib import Path


class Workspace:
    def __init__(self, root_path: str | Path | None = None):
        self.root_path = (
            Path(root_path).resolve()
            if root_path is not None
            else Path(tempfile.mkdtemp(prefix="workspace-")).resolve()
        )
        os.makedirs(self.root_path, exist_ok=True)

    def _safe(self, file_path: str) -> Path:
        p = (self.root_path / file_path).resolve()
        if not p.is_relative_to(self.root_path):
            raise ValueError(
                f"File path '{file_path}' is outside the workspace root. {self.root_path}"
            )
        return p

    def read_file(self, file_path: str):
        p = self._safe(file_path)
        return p.read_text() if p.is_file() else f"File '{file_path}' does not exist."

    def write_file(self, file_path: str, content: str):
        p = self._safe(file_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        return f"File '{file_path}' written successfully."

    def edit_file(
        self, file_path: str, new_content: str, old_content: str | None = None
    ):
        p = self._safe(file_path)
        if not p.is_file():
            return f"File '{file_path}' does not exist."

        current_content = p.read_text()

        if old_content is not None and current_content != old_content:
            return (
                f"File '{file_path}' content has changed since last read. Edit aborted."
            )

        p.write_text(
            current_content.replace(old_content, new_content)
            if old_content is not None
            else new_content
        )

        return f"File '{file_path}' edited successfully."
