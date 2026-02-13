"""Grid trading strategy — place buy and sell orders at intervals."""

from dataclasses import dataclass, field
from typing import List
from makemerich.strategies.base import BaseStrategy, Signal
from makemerich.core.logger import get_logger


@dataclass
class GridLevel:
    price: float
    side: str  # BUY or SELL
    filled: bool = False
    order_id: str = ""


class GridStrategy(BaseStrategy):
    """Grid trading — profit from price oscillation within a range."""

    name = "grid"

    def __init__(self, lower_price: float = 0, upper_price: float = 0,
                 num_grids: int = 10, total_investment: float = 1000):
        self.lower_price = lower_price
        self.upper_price = upper_price
        self.num_grids = num_grids
        self.total_investment = total_investment
        self.logger = get_logger("grid")
        self.levels: List[GridLevel] = []

    def setup_grid(self, lower: float, upper: float):
        """Initialize the grid levels."""
        self.lower_price = lower
        self.upper_price = upper
        step = (upper - lower) / self.num_grids

        self.levels = []
        for i in range(self.num_grids + 1):
            price = lower + (step * i)
            self.levels.append(GridLevel(
                price=round(price, 2),
                side="BUY" if i < self.num_grids // 2 else "SELL",
            ))

    def evaluate(self, analysis: dict, portfolio: dict) -> Signal:
        """Check if current price triggers a grid level."""
        price = analysis.get("current_price", 0)

        if not self.levels:
            return Signal(
                action="HOLD",
                pair=analysis.get("pair", ""),
                strength=0.0,
                reason="Grid not initialized. Call setup_grid() first.",
            )

        for level in self.levels:
            if not level.filled and abs(price - level.price) / level.price < 0.001:
                level.filled = True
                amount = self.total_investment / self.num_grids
                return Signal(
                    action=level.side,
                    pair=analysis.get("pair", ""),
                    strength=0.9,
                    reason=f"Grid {level.side} triggered at {level.price}",
                )

        return Signal(
            action="HOLD",
            pair=analysis.get("pair", ""),
            strength=0.0,
            reason=f"Price {price} not at any grid level",
        )
