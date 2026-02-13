"""Configuration management for MakeMeRich."""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional

import yaml
from dotenv import load_dotenv


load_dotenv()


@dataclass
class RiskConfig:
    max_risk_per_trade: float = 0.02
    max_positions: int = 5
    min_cash_percent: float = 30.0
    max_leverage: int = 1
    default_stop_loss_pct: float = 0.03


@dataclass
class LLMConfig:
    model: str = "claude-sonnet-4-5-20250929"
    max_tokens: int = 4096


@dataclass
class NotificationConfig:
    enabled: bool = False
    on_trade: bool = True
    on_error: bool = True
    daily_summary: bool = True


@dataclass
class Config:
    mode: str = "paper"
    cycle_interval: int = 60
    timeframe: str = "1h"
    trading_pairs: List[str] = field(default_factory=lambda: ["BTCUSDT", "ETHUSDT"])
    risk: RiskConfig = field(default_factory=RiskConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    notifications: NotificationConfig = field(default_factory=NotificationConfig)

    # API keys from environment
    binance_api_key: str = ""
    binance_api_secret: str = ""
    anthropic_api_key: str = ""
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    @classmethod
    def load(cls, config_path: str = "config/default.yaml") -> "Config":
        """Load configuration from YAML file and environment variables."""
        config = cls()

        # Load YAML config
        path = Path(config_path)
        if path.exists():
            with open(path) as f:
                data = yaml.safe_load(f) or {}

            config.mode = data.get("mode", config.mode)
            config.cycle_interval = data.get("cycle_interval", config.cycle_interval)
            config.timeframe = data.get("timeframe", config.timeframe)
            config.trading_pairs = data.get("trading_pairs", config.trading_pairs)

            if "risk" in data:
                risk = data["risk"]
                config.risk = RiskConfig(
                    max_risk_per_trade=risk.get("max_risk_per_trade", 0.02),
                    max_positions=risk.get("max_positions", 5),
                    min_cash_percent=risk.get("min_cash_percent", 30.0),
                    max_leverage=risk.get("max_leverage", 1),
                    default_stop_loss_pct=risk.get("default_stop_loss_pct", 0.03),
                )

            if "llm" in data:
                llm = data["llm"]
                config.llm = LLMConfig(
                    model=llm.get("model", "claude-sonnet-4-5-20250929"),
                    max_tokens=llm.get("max_tokens", 4096),
                )

        # Load API keys from environment
        config.binance_api_key = os.getenv("BINANCE_API_KEY", "")
        config.binance_api_secret = os.getenv("BINANCE_API_SECRET", "")
        config.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        config.telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        config.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "")

        return config
