"""Candlestick pattern detection skill."""

import pandas as pd
import numpy as np

from makemerich.skills.base import BaseSkill


class PatternDetectionSkill(BaseSkill):
    """Detect candlestick patterns in market data."""

    name = "pattern_detection"
    description = "Detect candlestick patterns (doji, hammer, engulfing, etc.)"

    def detect(self, klines: list) -> list:
        """Detect candlestick patterns in kline data."""
        if len(klines) < 3:
            return []

        df = pd.DataFrame(klines)
        patterns = []

        # Doji — open and close are very close
        last = df.iloc[-1]
        body = abs(last["close"] - last["open"])
        wick = last["high"] - last["low"]
        if wick > 0 and body / wick < 0.1:
            patterns.append({
                "pattern": "doji",
                "signal": "indecision",
                "confidence": 0.7,
            })

        # Hammer — small body at top, long lower wick
        if wick > 0:
            lower_wick = min(last["open"], last["close"]) - last["low"]
            upper_wick = last["high"] - max(last["open"], last["close"])
            if lower_wick > body * 2 and upper_wick < body * 0.5:
                patterns.append({
                    "pattern": "hammer",
                    "signal": "bullish_reversal",
                    "confidence": 0.65,
                })

        # Engulfing — current candle engulfs previous
        if len(df) >= 2:
            prev = df.iloc[-2]
            curr_bullish = last["close"] > last["open"]
            prev_bearish = prev["close"] < prev["open"]

            if curr_bullish and prev_bearish:
                if last["open"] <= prev["close"] and last["close"] >= prev["open"]:
                    patterns.append({
                        "pattern": "bullish_engulfing",
                        "signal": "bullish_reversal",
                        "confidence": 0.75,
                    })

            curr_bearish = last["close"] < last["open"]
            prev_bullish = prev["close"] > prev["open"]

            if curr_bearish and prev_bullish:
                if last["open"] >= prev["close"] and last["close"] <= prev["open"]:
                    patterns.append({
                        "pattern": "bearish_engulfing",
                        "signal": "bearish_reversal",
                        "confidence": 0.75,
                    })

        return patterns
