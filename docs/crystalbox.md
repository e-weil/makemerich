# CrystalBox — Transparency

CrystalBox is MakeMeRich's transparency layer. Every trading decision is logged with full reasoning, creating an immutable audit trail.

## How It Works

1. **Reasoning Capture** — Every time the AI makes a decision, its full chain of thought is captured
2. **Audit Log** — Decisions are written to a JSONL file with chained SHA-256 hashes
3. **Tamper Detection** — Like a mini-blockchain: if any entry is modified, the chain breaks

## Audit Log Format

Each entry in `data/crystalbox/audit.jsonl`:

```json
{
  "timestamp": "2025-01-15T10:30:00",
  "action": "BUY",
  "pair": "BTCUSDT",
  "amount": 0.01,
  "reasoning": "RSI at 28 (oversold), MACD crossing bullish, volume increasing...",
  "confidence": 0.82,
  "prev_hash": "abc123...",
  "hash": "def456..."
}
```

## Verifying the Chain

```python
from makemerich.crystalbox.audit import AuditLog
from pathlib import Path

audit = AuditLog(data_dir=Path("data/crystalbox"))
print(audit.verify_chain())  # True if untampered
```

## Reports

Generate human-readable reports:

```python
from makemerich.crystalbox.report import ReportGenerator

report = ReportGenerator(audit)
print(report.daily_report())
```

## Dashboard

View all decisions in the web dashboard:

```bash
uvicorn makemerich.web.app:app --reload
# Open http://localhost:8000
```
