"""Technical analysis skill — RSI, MACD, Bollinger Bands, and more."""

import pandas as pd
import numpy as np
import ta

from makemerich.skills.base import BaseSkill


class TechnicalAnalysisSkill(BaseSkill):
    """Calculates technical indicators from market data."""

    name = "technical_analysis"
    description = "Calculate technical indicators: RSI, MACD, Bollinger Bands, etc."

    def analyze(self, klines: list) -> dict:
        """Run full technical analysis on kline data."""
        if not klines:
            return {"error": "No data available"}

        df = pd.DataFrame(klines)
        close = df["close"]
        high = df["high"]
        low = df["low"]
        volume = df["volume"]

        current_price = close.iloc[-1]

        # RSI
        rsi = ta.momentum.RSIIndicator(close, window=14)
        rsi_value = round(rsi.rsi().iloc[-1], 2)

        # MACD
        macd = ta.trend.MACD(close)
        macd_value = round(macd.macd().iloc[-1], 4)
        macd_signal = round(macd.macd_signal().iloc[-1], 4)
        macd_hist = round(macd.macd_diff().iloc[-1], 4)
        macd_signal_str = "bullish" if macd_value > macd_signal else "bearish"

        # Bollinger Bands
        bb = ta.volatility.BollingerBands(close, window=20, window_dev=2)
        bb_upper = round(bb.bollinger_hband().iloc[-1], 2)
        bb_lower = round(bb.bollinger_lband().iloc[-1], 2)
        bb_middle = round(bb.bollinger_mavg().iloc[-1], 2)

        if current_price > bb_upper:
            bb_position = "above_upper"
        elif current_price < bb_lower:
            bb_position = "below_lower"
        else:
            bb_pct = (current_price - bb_lower) / (bb_upper - bb_lower)
            bb_position = f"middle ({round(bb_pct * 100)}%)"

        # Volume trend
        vol_sma = volume.rolling(window=20).mean().iloc[-1]
        current_vol = volume.iloc[-1]
        volume_trend = "above_average" if current_vol > vol_sma else "below_average"

        # 24h change approximation (last vs 24 candles ago for 1h timeframe)
        lookback = min(24, len(close) - 1)
        change_24h = round(
            ((current_price - close.iloc[-lookback - 1]) / close.iloc[-lookback - 1]) * 100, 2
        )

        # EMA
        ema_20 = round(ta.trend.EMAIndicator(close, window=20).ema_indicator().iloc[-1], 2)
        ema_50 = round(ta.trend.EMAIndicator(close, window=50).ema_indicator().iloc[-1], 2) if len(close) >= 50 else None

        # ATR
        atr = ta.volatility.AverageTrueRange(high, low, close, window=14)
        atr_value = round(atr.average_true_range().iloc[-1], 2)

        # Stochastic
        stoch = ta.momentum.StochasticOscillator(high, low, close)
        stoch_k = round(stoch.stoch().iloc[-1], 2)
        stoch_d = round(stoch.stoch_signal().iloc[-1], 2)

        return {
            "current_price": current_price,
            "rsi": rsi_value,
            "rsi_signal": "oversold" if rsi_value < 30 else "overbought" if rsi_value > 70 else "neutral",
            "macd": macd_value,
            "macd_signal": macd_signal_str,
            "macd_histogram": macd_hist,
            "bb_upper": bb_upper,
            "bb_lower": bb_lower,
            "bb_middle": bb_middle,
            "bb_position": bb_position,
            "volume_trend": volume_trend,
            "change_24h": change_24h,
            "ema_20": ema_20,
            "ema_50": ema_50,
            "atr": atr_value,
            "stoch_k": stoch_k,
            "stoch_d": stoch_d,
        }

    def detailed_analysis(self, symbol: str, timeframe: str = "1h") -> dict:
        """Placeholder for detailed analysis — requires market data skill."""
        return {"info": f"Detailed analysis for {symbol} on {timeframe} requires market data"}
