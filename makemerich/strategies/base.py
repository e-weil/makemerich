"""Base class for trading strategies."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class Signal:
    action: str           # BUY, SELL, HOLD
    pair: str
    strength: float       # 0.0 to 1.0
    reason: str
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None


class BaseStrategy(ABC):
    """Base class for all trading strategies."""

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def evaluate(self, analysis: dict, portfolio: dict) -> Signal:
        """Evaluate market data and return a trading signal."""
        ...
