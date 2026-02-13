"""Tests for trading strategies."""

import pytest
from makemerich.strategies.momentum import MomentumStrategy
from makemerich.strategies.mean_reversion import MeanReversionStrategy
from makemerich.strategies.dca import DCAStrategy


class TestMomentumStrategy:
    def setup_method(self):
        self.strategy = MomentumStrategy()

    def test_buy_signal(self):
        analysis = {
            "rsi": 25,
            "macd_signal": "bullish",
            "volume_trend": "above_average",
            "current_price": 50000,
            "pair": "BTCUSDT",
        }
        signal = self.strategy.evaluate(analysis, {})
        assert signal.action == "BUY"
        assert signal.strength > 0
        assert signal.stop_loss is not None

    def test_sell_signal(self):
        analysis = {
            "rsi": 80,
            "macd_signal": "bearish",
            "volume_trend": "normal",
            "current_price": 50000,
            "pair": "BTCUSDT",
        }
        signal = self.strategy.evaluate(analysis, {})
        assert signal.action == "SELL"

    def test_hold_signal(self):
        analysis = {
            "rsi": 50,
            "macd_signal": "neutral",
            "volume_trend": "normal",
            "current_price": 50000,
            "pair": "BTCUSDT",
        }
        signal = self.strategy.evaluate(analysis, {})
        assert signal.action == "HOLD"


class TestMeanReversionStrategy:
    def setup_method(self):
        self.strategy = MeanReversionStrategy()

    def test_buy_at_lower_band(self):
        analysis = {
            "bb_position": "below_lower",
            "rsi": 25,
            "current_price": 48000,
            "bb_middle": 50000,
            "pair": "BTCUSDT",
        }
        signal = self.strategy.evaluate(analysis, {})
        assert signal.action == "BUY"

    def test_hold_in_middle(self):
        analysis = {
            "bb_position": "middle (50%)",
            "rsi": 50,
            "current_price": 50000,
            "pair": "BTCUSDT",
        }
        signal = self.strategy.evaluate(analysis, {})
        assert signal.action == "HOLD"


class TestDCAStrategy:
    def test_first_buy(self):
        strategy = DCAStrategy(base_amount=100, interval_hours=24)
        analysis = {
            "change_24h": -1.0,
            "current_price": 50000,
            "pair": "BTCUSDT",
        }
        signal = strategy.evaluate(analysis, {})
        assert signal.action == "BUY"

    def test_dip_multiplier(self):
        strategy = DCAStrategy(base_amount=100, dip_threshold=-5.0, dip_multiplier=2.0)
        analysis = {
            "change_24h": -8.0,
            "current_price": 46000,
            "pair": "BTCUSDT",
        }
        signal = strategy.evaluate(analysis, {})
        assert signal.action == "BUY"
        assert "dip mode" in signal.reason
