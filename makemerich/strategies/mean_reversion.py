"""Mean reversion strategy — buy low, sell high relative to the mean."""

from makemerich.strategies.base import BaseStrategy, Signal


class MeanReversionStrategy(BaseStrategy):
    """Buy when price is below the mean, sell when above."""

    name = "mean_reversion"

    def __init__(self, bb_buy_threshold: str = "below_lower",
                 bb_sell_threshold: str = "above_upper"):
        self.bb_buy_threshold = bb_buy_threshold
        self.bb_sell_threshold = bb_sell_threshold

    def evaluate(self, analysis: dict, portfolio: dict) -> Signal:
        """Generate signal based on Bollinger Bands position."""
        bb_position = analysis.get("bb_position", "middle")
        rsi = analysis.get("rsi", 50)
        price = analysis.get("current_price", 0)

        if bb_position == self.bb_buy_threshold and rsi < 35:
            return Signal(
                action="BUY",
                pair=analysis.get("pair", ""),
                strength=0.8,
                reason=f"Mean reversion buy: price {bb_position}, RSI={rsi} oversold",
                stop_loss=price * 0.96,
                take_profit=analysis.get("bb_middle", price * 1.03),
            )

        if bb_position == self.bb_sell_threshold and rsi > 65:
            return Signal(
                action="SELL",
                pair=analysis.get("pair", ""),
                strength=0.8,
                reason=f"Mean reversion sell: price {bb_position}, RSI={rsi} overbought",
            )

        return Signal(
            action="HOLD",
            pair=analysis.get("pair", ""),
            strength=0.0,
            reason=f"No mean reversion signal: BB={bb_position}, RSI={rsi}",
        )
