"""
MakeMeRich Engine — The trading Gateway.

Equivalent to the Gateway in OpenClaw:
- OpenClaw: receives message -> LLM decides -> executes skill (email, calendar)
- MakeMeRich: receives market signal -> LLM decides -> executes skill (buy, sell)
"""

import asyncio
from datetime import datetime
from pathlib import Path

from makemerich.core.config import Config
from makemerich.core.session import Session
from makemerich.core.logger import get_logger
from makemerich.agent.trader import TraderAgent
from makemerich.agent.risk import RiskManager
from makemerich.skills.binance.market_data import MarketDataSkill
from makemerich.skills.binance.spot import SpotTradingSkill
from makemerich.skills.binance.account import AccountSkill
from makemerich.skills.analysis.technical import TechnicalAnalysisSkill
from makemerich.crystalbox.reasoning import ReasoningCapture
from makemerich.crystalbox.audit import AuditLog


class Engine:
    """Main MakeMeRich engine."""

    def __init__(self, config_path: str = "config/default.yaml"):
        self.config = Config.load(config_path)
        self.logger = get_logger("engine")
        self.session = Session(data_dir=Path("data/sessions"))
        self.audit = AuditLog(data_dir=Path("data/crystalbox"))
        self.reasoning = ReasoningCapture()
        self.risk = RiskManager(self.config)

        # Initialize skills (equivalent to OpenClaw channel adapters)
        self.skills = {
            "market_data": MarketDataSkill(self.config),
            "spot_trading": SpotTradingSkill(self.config),
            "account": AccountSkill(self.config),
            "technical": TechnicalAnalysisSkill(),
        }

        # Initialize agent (the brain)
        self.agent = TraderAgent(
            config=self.config,
            skills=self.skills,
            reasoning=self.reasoning,
        )

        self.running = False

    async def start(self):
        """Start the trading engine."""
        self.running = True
        self.logger.info("MakeMeRich Engine starting",
                        mode=self.config.mode,
                        pairs=self.config.trading_pairs)

        # Verify Binance connection
        account = await self.skills["account"].get_balance()
        self.logger.info("Connected to Binance", balance=account)

        # Main loop
        while self.running:
            try:
                await self._trading_cycle()
                await asyncio.sleep(self.config.cycle_interval)
            except KeyboardInterrupt:
                self.logger.info("Shutting down...")
                self.running = False
            except Exception as e:
                self.logger.error("Error in trading cycle", error=str(e))
                await asyncio.sleep(60)

    async def _trading_cycle(self):
        """One complete cycle: analyze -> decide -> execute."""

        # 1. Get market data
        market_data = {}
        for pair in self.config.trading_pairs:
            market_data[pair] = await self.skills["market_data"].get_klines(
                symbol=pair,
                interval=self.config.timeframe,
                limit=100,
            )

        # 2. Technical analysis
        analysis = {}
        for pair, data in market_data.items():
            analysis[pair] = self.skills["technical"].analyze(data)

        # 3. Agent decides (LLM)
        decision = await self.agent.decide(
            market_data=market_data,
            analysis=analysis,
            session=self.session,
        )

        # 4. CrystalBox — capture reasoning
        self.reasoning.capture(decision)
        self.audit.log(decision)

        # 5. Execute trade if the agent decided to act
        if decision.action != "HOLD":
            if self.config.mode == "live":
                result = await self.skills["spot_trading"].execute(decision)
                self.logger.info("Trade executed",
                               action=decision.action,
                               pair=decision.pair,
                               amount=decision.amount,
                               reason=decision.reasoning)
            else:
                self.logger.info("Paper trade",
                               action=decision.action,
                               pair=decision.pair,
                               reason=decision.reasoning)

    async def stop(self):
        self.running = False
