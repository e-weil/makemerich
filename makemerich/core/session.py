"""Session persistence using JSONL — same pattern as OpenClaw."""

import json
from datetime import datetime
from pathlib import Path
from typing import List


class Session:
    """Persistent session manager using JSONL files."""

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._session_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        self._file = self.data_dir / f"session_{self._session_id}.jsonl"
        self._messages: List[dict] = []

    @property
    def session_id(self) -> str:
        return self._session_id

    def append(self, message: dict):
        """Append a message to the session."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            **message,
        }
        self._messages.append(entry)

    def save(self):
        """Persist session to JSONL file."""
        with open(self._file, "w") as f:
            for msg in self._messages:
                f.write(json.dumps(msg) + "\n")

    def load(self) -> List[dict]:
        """Load messages from current session."""
        return [
            {"role": m["role"], "content": m["content"]}
            for m in self._messages
            if "role" in m and "content" in m
        ]

    def load_from_file(self, filepath: Path) -> List[dict]:
        """Load a previous session from file."""
        messages = []
        if filepath.exists():
            with open(filepath) as f:
                for line in f:
                    entry = json.loads(line)
                    if "role" in entry and "content" in entry:
                        messages.append({
                            "role": entry["role"],
                            "content": entry["content"],
                        })
        self._messages = messages
        return messages

    def list_sessions(self) -> List[str]:
        """List all available sessions."""
        return sorted([
            f.stem.replace("session_", "")
            for f in self.data_dir.glob("session_*.jsonl")
        ])
