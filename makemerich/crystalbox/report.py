"""CrystalBox Report — Generates human-readable reports of trading decisions."""

from datetime import datetime
from pathlib import Path

from makemerich.crystalbox.audit import AuditLog


class ReportGenerator:
    """Generate readable reports from the audit log."""

    def __init__(self, audit: AuditLog):
        self.audit = audit

    def daily_report(self, date: str = None) -> str:
        """Generate a daily trading report."""
        if date is None:
            date = datetime.utcnow().strftime("%Y-%m-%d")

        history = self.audit.get_history(limit=1000)
        day_entries = [e for e in history if e["timestamp"].startswith(date)]

        if not day_entries:
            return f"# Trading Report — {date}\n\nNo trades today."

        report = f"# Trading Report — {date}\n\n"
        report += f"**Total decisions:** {len(day_entries)}\n\n"

        trades = [e for e in day_entries if e["action"] != "HOLD"]
        holds = [e for e in day_entries if e["action"] == "HOLD"]

        report += f"**Trades executed:** {len(trades)}\n"
        report += f"**Hold decisions:** {len(holds)}\n\n"

        if trades:
            report += "## Trades\n\n"
            for t in trades:
                report += f"### {t['action']} {t['pair']}\n"
                report += f"- **Time:** {t['timestamp']}\n"
                report += f"- **Amount:** {t['amount']}\n"
                report += f"- **Confidence:** {t['confidence']}\n"
                report += f"- **Reasoning:** {t['reasoning']}\n\n"

        # Chain integrity
        chain_valid = self.audit.verify_chain()
        report += f"\n---\n**Audit chain integrity:** {'VALID' if chain_valid else 'BROKEN'}\n"

        return report

    def trade_report(self, trade_hash: str) -> str:
        """Generate a report for a specific trade by its hash."""
        history = self.audit.get_history(limit=10000)
        for entry in history:
            if entry.get("hash") == trade_hash:
                report = f"# Trade Report\n\n"
                report += f"- **Hash:** {trade_hash}\n"
                report += f"- **Action:** {entry['action']}\n"
                report += f"- **Pair:** {entry['pair']}\n"
                report += f"- **Amount:** {entry['amount']}\n"
                report += f"- **Time:** {entry['timestamp']}\n"
                report += f"- **Confidence:** {entry['confidence']}\n\n"
                report += f"## Reasoning\n\n{entry['reasoning']}\n"
                return report
        return f"Trade with hash {trade_hash} not found."
