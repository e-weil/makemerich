"""
TraderAgent — The brain that decides.

In OpenClaw: user sends message -> LLM interprets -> decides which skill to use
In MakeMeRich: market sends data -> LLM interprets -> decides which trade to make
"""

import json
from dataclasses import dataclass
from typing import Optional

import anthropic

from makemerich.agent.soul import load_soul
from makemerich.crystalbox.reasoning import ReasoningCapture


@dataclass
class TradeDecision:
    action: str           # BUY, SELL, HOLD
    pair: str             # BTCUSDT, ETHUSDT, etc.
    amount: float         # Quantity
    price: Optional[float]  # Limit price (None = market)
    stop_loss: Optional[float]
    take_profit: Optional[float]
    reasoning: str        # WHY — the CrystalBox
    confidence: float     # 0.0 to 1.0
    raw_analysis: dict    # Full analysis data


TRADING_TOOLS = [
    {
        "name": "execute_spot_buy",
        "description": "Buy a cryptocurrency on the Binance spot market",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "Trading pair, e.g. BTCUSDT"},
                "amount_usdt": {"type": "number", "description": "Amount in USDT to invest"},
                "order_type": {"type": "string", "enum": ["market", "limit"],
                              "description": "Order type"},
                "limit_price": {"type": "number", "description": "Limit price (only for limit orders)"},
            },
            "required": ["symbol", "amount_usdt", "order_type"]
        }
    },
    {
        "name": "execute_spot_sell",
        "description": "Sell a cryptocurrency on the Binance spot market",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "Trading pair, e.g. BTCUSDT"},
                "amount": {"type": "number", "description": "Amount of the asset to sell"},
                "order_type": {"type": "string", "enum": ["market", "limit"]},
                "limit_price": {"type": "number", "description": "Limit price"},
            },
            "required": ["symbol", "amount", "order_type"]
        }
    },
    {
        "name": "set_stop_loss",
        "description": "Set a stop-loss for an open position",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string"},
                "stop_price": {"type": "number", "description": "Stop activation price"},
                "amount": {"type": "number", "description": "Amount to sell at stop"},
            },
            "required": ["symbol", "stop_price", "amount"]
        }
    },
    {
        "name": "get_portfolio",
        "description": "View current portfolio: balances, open positions, P&L",
        "input_schema": {
            "type": "object",
            "properties": {},
        }
    },
    {
        "name": "get_market_analysis",
        "description": "Get detailed technical analysis for a pair",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "Pair to analyze"},
                "timeframe": {"type": "string", "enum": ["1m", "5m", "15m", "1h", "4h", "1d"],
                             "description": "Analysis timeframe"},
            },
            "required": ["symbol"]
        }
    },
]


class TraderAgent:
    """The agent that decides trades using an LLM."""

    def __init__(self, config, skills, reasoning: ReasoningCapture):
        self.config = config
        self.skills = skills
        self.reasoning = reasoning
        self.client = anthropic.Anthropic()
        self.soul = load_soul()

    async def decide(self, market_data: dict, analysis: dict, session) -> TradeDecision:
        """
        Agent decision cycle.
        Same pattern as run_agent_turn() in OpenClaw.
        """
        context = self._build_context(market_data, analysis)

        messages = session.load()
        messages.append({"role": "user", "content": context})

        # Agent loop (same as OpenClaw: LLM -> tool -> LLM -> tool -> response)
        while True:
            response = self.client.messages.create(
                model=self.config.llm.model,
                max_tokens=self.config.llm.max_tokens,
                system=self.soul,
                tools=TRADING_TOOLS,
                messages=messages,
            )

            if response.stop_reason == "end_turn":
                decision = self._parse_decision(response)
                session.append({"role": "assistant",
                               "content": self._serialize_content(response.content)})
                session.save()
                return decision

            if response.stop_reason == "tool_use":
                messages.append({"role": "assistant",
                                "content": self._serialize_content(response.content)})

                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        result = await self._execute_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result),
                        })

                messages.append({"role": "user", "content": tool_results})

    async def _execute_tool(self, name: str, input_data: dict) -> dict:
        """Execute a trading skill."""
        if name == "execute_spot_buy":
            return await self.skills["spot_trading"].buy(
                symbol=input_data["symbol"],
                amount_usdt=input_data["amount_usdt"],
                order_type=input_data["order_type"],
                limit_price=input_data.get("limit_price"),
            )
        elif name == "execute_spot_sell":
            return await self.skills["spot_trading"].sell(
                symbol=input_data["symbol"],
                amount=input_data["amount"],
                order_type=input_data["order_type"],
                limit_price=input_data.get("limit_price"),
            )
        elif name == "get_portfolio":
            return await self.skills["account"].get_portfolio()
        elif name == "get_market_analysis":
            return self.skills["technical"].detailed_analysis(
                symbol=input_data["symbol"],
                timeframe=input_data.get("timeframe", "1h"),
            )
        elif name == "set_stop_loss":
            return await self.skills["spot_trading"].set_stop_loss(
                symbol=input_data["symbol"],
                stop_price=input_data["stop_price"],
                amount=input_data["amount"],
            )
        return {"error": f"Unknown tool: {name}"}

    def _build_context(self, market_data: dict, analysis: dict) -> str:
        """Build the context prompt for the LLM."""
        context = "## Market Update\n\n"
        for pair, data in analysis.items():
            context += f"### {pair}\n"
            context += f"Price: ${data.get('current_price', 'N/A')}\n"
            context += f"RSI(14): {data.get('rsi', 'N/A')}\n"
            context += f"MACD Signal: {data.get('macd_signal', 'N/A')}\n"
            context += f"Bollinger: {data.get('bb_position', 'N/A')}\n"
            context += f"Volume trend: {data.get('volume_trend', 'N/A')}\n"
            context += f"24h Change: {data.get('change_24h', 'N/A')}%\n\n"
        context += "Based on this data, analyze the market and decide your action. "
        context += "Use the available tools to execute trades or gather more information. "
        context += "ALWAYS explain your reasoning in detail (CrystalBox).\n"
        return context

    def _parse_decision(self, response) -> TradeDecision:
        """Parse the LLM response into a TradeDecision."""
        text = ""
        for block in response.content:
            if hasattr(block, "text"):
                text += block.text

        return TradeDecision(
            action="HOLD",
            pair="",
            amount=0,
            price=None,
            stop_loss=None,
            take_profit=None,
            reasoning=text,
            confidence=0.5,
            raw_analysis={},
        )

    def _serialize_content(self, content) -> list:
        serialized = []
        for block in content:
            if hasattr(block, "text"):
                serialized.append({"type": "text", "text": block.text})
            elif block.type == "tool_use":
                serialized.append({
                    "type": "tool_use",
                    "id": block.id,
                    "name": block.name,
                    "input": block.input,
                })
        return serialized
