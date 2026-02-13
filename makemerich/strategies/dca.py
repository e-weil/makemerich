"""Dollar Cost Averaging strategy — intelligent recurring buys."""

from datetime import datetime, timedelta
from makemerich.strategies.base import BaseStrategy, Signal
from makemerich.core.logger import get_logger


class DCAStrategy(BaseStrategy):
    """Smart DCA — buy at regular intervals, increase size on dips."""

    name = "dca"

    def __init__(self, base_amount: float = 100, interval_hours: int = 24,
                 dip_multiplier: float = 1.5, dip_threshold: float = -5.0):
        self.base_amount = base_amount
        self.interval_hours = interval_hours
        self.dip_multiplier = dip_multiplier
        self.dip_threshold = dip_threshold
        self.logger = get_logger("dca")
        self._last_buy: datetime = None

    def evaluate(self, analysis: dict, portfolio: dict) -> Signal:
        """Check if it's time for a DCA buy."""
        now = datetime.utcnow()

        # Check if interval has passed
        if self._last_buy:
            elapsed = (now - self._last_buy).total_seconds() / 3600
            if elapsed < self.interval_hours:
                hours_left = self.interval_hours - elapsed
                return Signal(
                    action="HOLD",
                    pair=analysis.get("pair", ""),
                    strength=0.0,
                    reason=f"DCA: next buy in {hours_left:.1f} hours",
                )

        # Determine amount — increase on dips
        change_24h = analysis.get("change_24h", 0)
        amount = self.base_amount
        if change_24h < self.dip_threshold:
            amount *= self.dip_multiplier
            reason = f"DCA buy (dip mode): {change_24h}% 24h change, amount ${amount}"
        else:
            reason = f"DCA buy (regular): scheduled interval reached, amount ${amount}"

        price = analysis.get("current_price", 0)
        self._last_buy = now

        return Signal(
            action="BUY",
            pair=analysis.get("pair", ""),
            strength=0.6,
            reason=reason,
            stop_loss=price * 0.95 if price else None,
        )
