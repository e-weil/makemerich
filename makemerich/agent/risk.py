"""Risk management — enforces position sizing and risk rules."""

from dataclasses import dataclass
from typing import Optional

from makemerich.core.logger import get_logger


@dataclass
class RiskAssessment:
    approved: bool
    max_position_size: float
    stop_loss_price: Optional[float]
    reason: str


class RiskManager:
    """Enforces risk management rules. Never violate these."""

    def __init__(self, config):
        self.config = config
        self.logger = get_logger("risk")

    def assess_trade(self, action: str, pair: str, amount: float,
                     entry_price: float, portfolio_value: float,
                     open_positions: int) -> RiskAssessment:
        """Assess whether a trade meets risk requirements."""

        # Rule: Max positions
        if open_positions >= self.config.risk.max_positions:
            return RiskAssessment(
                approved=False,
                max_position_size=0,
                stop_loss_price=None,
                reason=f"Max positions ({self.config.risk.max_positions}) reached",
            )

        # Rule: Max risk per trade
        max_risk_amount = portfolio_value * self.config.risk.max_risk_per_trade
        stop_loss_pct = self.config.risk.default_stop_loss_pct
        max_position = max_risk_amount / stop_loss_pct

        if amount > max_position:
            self.logger.warning("Position size exceeds max risk",
                              requested=amount, max_allowed=max_position)

        # Rule: Min cash percent
        cash_after_trade = portfolio_value - amount
        min_cash = portfolio_value * (self.config.risk.min_cash_percent / 100)
        if cash_after_trade < min_cash:
            adjusted = portfolio_value - min_cash
            if adjusted <= 0:
                return RiskAssessment(
                    approved=False,
                    max_position_size=0,
                    stop_loss_price=None,
                    reason=f"Would violate min cash rule ({self.config.risk.min_cash_percent}%)",
                )
            max_position = min(max_position, adjusted)

        # Calculate stop-loss price
        stop_loss_price = entry_price * (1 - stop_loss_pct)

        final_size = min(amount, max_position)

        return RiskAssessment(
            approved=True,
            max_position_size=final_size,
            stop_loss_price=stop_loss_price,
            reason="Trade approved within risk parameters",
        )
