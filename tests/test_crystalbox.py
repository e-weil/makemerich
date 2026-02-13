"""Tests for CrystalBox audit log."""

import pytest
import json
from pathlib import Path
from dataclasses import dataclass
from makemerich.crystalbox.audit import AuditLog


@dataclass
class MockDecision:
    action: str = "BUY"
    pair: str = "BTCUSDT"
    amount: float = 0.1
    reasoning: str = "Test reasoning"
    confidence: float = 0.8


class TestAuditLog:
    def test_log_decision(self, tmp_path):
        audit = AuditLog(data_dir=tmp_path)
        decision = MockDecision()
        hash_val = audit.log(decision)

        assert hash_val is not None
        assert len(hash_val) == 64  # SHA256 hex

    def test_chain_integrity(self, tmp_path):
        audit = AuditLog(data_dir=tmp_path)

        for i in range(5):
            audit.log(MockDecision(amount=i))

        assert audit.verify_chain() is True

    def test_tamper_detection(self, tmp_path):
        audit = AuditLog(data_dir=tmp_path)
        audit.log(MockDecision())
        audit.log(MockDecision(action="SELL"))

        # Tamper with the log
        log_file = tmp_path / "audit.jsonl"
        lines = log_file.read_text().strip().split("\n")
        entry = json.loads(lines[0])
        entry["amount"] = 999
        lines[0] = json.dumps(entry)
        log_file.write_text("\n".join(lines) + "\n")

        assert audit.verify_chain() is False

    def test_get_history(self, tmp_path):
        audit = AuditLog(data_dir=tmp_path)
        audit.log(MockDecision(pair="BTCUSDT"))
        audit.log(MockDecision(pair="ETHUSDT"))
        audit.log(MockDecision(pair="BTCUSDT"))

        all_history = audit.get_history()
        assert len(all_history) == 3

        btc_history = audit.get_history(pair="BTCUSDT")
        assert len(btc_history) == 2

    def test_empty_log_is_valid(self, tmp_path):
        audit = AuditLog(data_dir=tmp_path)
        assert audit.verify_chain() is True
