"""Momentum strategy — ride the trend."""

from makemerich.strategies.base import BaseStrategy, Signal


class MomentumStrategy(BaseStrategy):
    """Buy when momentum is strong and trending up, sell when it fades."""

    name = "momentum"

    def __init__(self, rsi_buy_threshold: float = 40, rsi_sell_threshold: float = 70,
                 require_macd_confirm: bool = True):
        self.rsi_buy_threshold = rsi_buy_threshold
        self.rsi_sell_threshold = rsi_sell_threshold
        self.require_macd_confirm = require_macd_confirm

    def evaluate(self, analysis: dict, portfolio: dict) -> Signal:
        """Generate signal based on momentum indicators."""
        rsi = analysis.get("rsi", 50)
        macd_signal = analysis.get("macd_signal", "neutral")
        volume_trend = analysis.get("volume_trend", "normal")
        price = analysis.get("current_price", 0)

        # Buy signal: RSI recovering from oversold + MACD bullish
        if rsi < self.rsi_buy_threshold and macd_signal == "bullish":
            strength = min((self.rsi_buy_threshold - rsi) / 30, 1.0)
            if volume_trend == "above_average":
                strength = min(strength + 0.2, 1.0)
            return Signal(
                action="BUY",
                pair=analysis.get("pair", ""),
                strength=strength,
                reason=f"Momentum buy: RSI={rsi} recovering, MACD bullish, volume {volume_trend}",
                stop_loss=price * 0.97,
                take_profit=price * 1.06,
            )

        # Sell signal: RSI overbought + MACD bearish
        if rsi > self.rsi_sell_threshold and macd_signal == "bearish":
            strength = min((rsi - self.rsi_sell_threshold) / 30, 1.0)
            return Signal(
                action="SELL",
                pair=analysis.get("pair", ""),
                strength=strength,
                reason=f"Momentum sell: RSI={rsi} overbought, MACD bearish",
            )

        return Signal(
            action="HOLD",
            pair=analysis.get("pair", ""),
            strength=0.0,
            reason=f"No momentum signal: RSI={rsi}, MACD={macd_signal}",
        )
