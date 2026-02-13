"""
CrystalBox Audit Log — Total transparency.

Every trade has an immutable reasoning chain.
This is what NO open source trading bot offers.
The user sees exactly WHY every operation was made.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path


class AuditLog:
    """Immutable log of trading decisions."""

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = data_dir / "audit.jsonl"
        self._last_hash = self._get_last_hash()

    def log(self, decision) -> str:
        """Log a decision with chained hash (tamper-evident)."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": decision.action,
            "pair": decision.pair,
            "amount": decision.amount,
            "reasoning": decision.reasoning,
            "confidence": decision.confidence,
            "prev_hash": self._last_hash,
        }

        entry_str = json.dumps(entry, sort_keys=True)
        entry["hash"] = hashlib.sha256(entry_str.encode()).hexdigest()
        self._last_hash = entry["hash"]

        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

        return entry["hash"]

    def verify_chain(self) -> bool:
        """Verify that nobody has tampered with the log."""
        if not self.log_file.exists():
            return True

        prev_hash = "genesis"
        with open(self.log_file) as f:
            for line in f:
                entry = json.loads(line)
                stored_hash = entry.pop("hash")
                if entry["prev_hash"] != prev_hash:
                    return False
                computed = hashlib.sha256(
                    json.dumps(entry, sort_keys=True).encode()
                ).hexdigest()
                if computed != stored_hash:
                    return False
                prev_hash = stored_hash
        return True

    def get_history(self, pair: str = None, limit: int = 50) -> list:
        """Get decision history."""
        entries = []
        if self.log_file.exists():
            with open(self.log_file) as f:
                for line in f:
                    entry = json.loads(line)
                    if pair is None or entry["pair"] == pair:
                        entries.append(entry)
        return entries[-limit:]

    def _get_last_hash(self) -> str:
        if not self.log_file.exists():
            return "genesis"
        with open(self.log_file) as f:
            lines = f.readlines()
            if lines:
                return json.loads(lines[-1])["hash"]
        return "genesis"
