"""CrystalBox Reasoning — Captures the reasoning chain for every trade decision."""

from datetime import datetime
from makemerich.core.logger import get_logger


class ReasoningCapture:
    """Captures and stores the reasoning chain for each trading decision."""

    def __init__(self):
        self.logger = get_logger("crystalbox")
        self._chain: list = []

    def capture(self, decision) -> dict:
        """Capture the reasoning behind a trading decision."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": decision.action,
            "pair": decision.pair,
            "confidence": decision.confidence,
            "reasoning": decision.reasoning,
            "analysis_summary": decision.raw_analysis,
        }
        self._chain.append(entry)
        self.logger.info("Reasoning captured",
                        action=decision.action,
                        pair=decision.pair,
                        confidence=decision.confidence)
        return entry

    def get_chain(self, limit: int = 20) -> list:
        """Get the most recent reasoning chain entries."""
        return self._chain[-limit:]

    def clear(self):
        """Clear the in-memory reasoning chain."""
        self._chain = []
