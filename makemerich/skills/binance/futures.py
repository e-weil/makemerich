"""Binance Futures trading skill — for leverage trading (use with caution)."""

from binance.client import Client

from makemerich.skills.base import BaseSkill


class FuturesTradingSkill(BaseSkill):
    """Connects to Binance Futures. Use with extreme caution."""

    name = "futures_trading"
    description = "Execute futures trades on Binance (leverage trading)"

    def __init__(self, config):
        self.client = Client(
            config.binance_api_key,
            config.binance_api_secret,
            testnet=config.mode == "paper",
        )
        self.config = config

    async def open_long(self, symbol: str, amount_usdt: float,
                        leverage: int = 1) -> dict:
        """Open a long position."""
        try:
            self.client.futures_change_leverage(symbol=symbol, leverage=leverage)
            order = self.client.futures_create_order(
                symbol=symbol,
                side="BUY",
                type="MARKET",
                quantity=amount_usdt,
            )
            return {"status": "success", "order": order}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def open_short(self, symbol: str, amount_usdt: float,
                         leverage: int = 1) -> dict:
        """Open a short position."""
        try:
            self.client.futures_change_leverage(symbol=symbol, leverage=leverage)
            order = self.client.futures_create_order(
                symbol=symbol,
                side="SELL",
                type="MARKET",
                quantity=amount_usdt,
            )
            return {"status": "success", "order": order}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def close_position(self, symbol: str) -> dict:
        """Close an open futures position."""
        try:
            positions = self.client.futures_position_information(symbol=symbol)
            for pos in positions:
                amt = float(pos["positionAmt"])
                if amt != 0:
                    side = "SELL" if amt > 0 else "BUY"
                    order = self.client.futures_create_order(
                        symbol=symbol,
                        side=side,
                        type="MARKET",
                        quantity=abs(amt),
                    )
                    return {"status": "success", "order": order}
            return {"status": "info", "message": "No open position"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
