"""Tests for the MakeMeRich engine."""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from makemerich.core.config import Config, RiskConfig


class TestConfig:
    def test_default_config(self):
        config = Config()
        assert config.mode == "paper"
        assert config.cycle_interval == 60
        assert config.timeframe == "1h"
        assert "BTCUSDT" in config.trading_pairs

    def test_risk_defaults(self):
        config = Config()
        assert config.risk.max_risk_per_trade == 0.02
        assert config.risk.max_positions == 5
        assert config.risk.min_cash_percent == 30.0
        assert config.risk.max_leverage == 1

    def test_load_from_yaml(self, tmp_path):
        yaml_content = """
mode: live
cycle_interval: 30
trading_pairs:
  - BTCUSDT
risk:
  max_risk_per_trade: 0.01
  max_positions: 3
"""
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text(yaml_content)

        config = Config.load(str(config_file))
        assert config.mode == "live"
        assert config.cycle_interval == 30
        assert config.risk.max_risk_per_trade == 0.01
        assert config.risk.max_positions == 3
