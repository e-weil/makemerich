"""
Skill de Binance Spot — Equivalent to a channel adapter in OpenClaw.

In OpenClaw: WhatsApp adapter receives/sends messages
In MakeMeRich: Binance adapter receives data / executes trades
"""

from binance.client import Client
from binance.enums import (
    SIDE_SELL,
    ORDER_TYPE_STOP_LOSS_LIMIT,
    TIME_IN_FORCE_GTC,
)

from makemerich.skills.base import BaseSkill


class SpotTradingSkill(BaseSkill):
    """Connects to Binance for spot trading."""

    name = "spot_trading"
    description = "Execute spot trades on Binance"

    def __init__(self, config):
        self.client = Client(
            config.binance_api_key,
            config.binance_api_secret,
            testnet=config.mode == "paper",
        )
        self.config = config

    async def buy(self, symbol: str, amount_usdt: float,
                  order_type: str = "market", limit_price: float = None) -> dict:
        """Execute a buy order."""
        try:
            if order_type == "market":
                order = self.client.order_market_buy(
                    symbol=symbol,
                    quoteOrderQty=amount_usdt,
                )
            else:
                qty = round(amount_usdt / limit_price, 6)
                order = self.client.order_limit_buy(
                    symbol=symbol,
                    quantity=qty,
                    price=str(limit_price),
                )

            return {
                "status": "success",
                "order_id": order["orderId"],
                "symbol": symbol,
                "side": "BUY",
                "type": order_type,
                "executed_qty": order.get("executedQty"),
                "price": order.get("price") or order.get("fills", [{}])[0].get("price"),
                "raw": order,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def sell(self, symbol: str, amount: float,
                   order_type: str = "market", limit_price: float = None) -> dict:
        """Execute a sell order."""
        try:
            if order_type == "market":
                order = self.client.order_market_sell(
                    symbol=symbol,
                    quantity=amount,
                )
            else:
                order = self.client.order_limit_sell(
                    symbol=symbol,
                    quantity=amount,
                    price=str(limit_price),
                )

            return {
                "status": "success",
                "order_id": order["orderId"],
                "symbol": symbol,
                "side": "SELL",
                "type": order_type,
                "executed_qty": order.get("executedQty"),
                "price": order.get("price") or order.get("fills", [{}])[0].get("price"),
                "raw": order,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def set_stop_loss(self, symbol: str, stop_price: float,
                            amount: float) -> dict:
        """Set a stop-loss order."""
        try:
            order = self.client.create_order(
                symbol=symbol,
                side=SIDE_SELL,
                type=ORDER_TYPE_STOP_LOSS_LIMIT,
                quantity=amount,
                stopPrice=str(stop_price),
                price=str(stop_price * 0.999),
                timeInForce=TIME_IN_FORCE_GTC,
            )
            return {"status": "success", "order_id": order["orderId"], "raw": order}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def get_open_orders(self, symbol: str = None) -> list:
        """Get open orders."""
        if symbol:
            return self.client.get_open_orders(symbol=symbol)
        return self.client.get_open_orders()

    async def cancel_order(self, symbol: str, order_id: int) -> dict:
        """Cancel an order."""
        try:
            result = self.client.cancel_order(symbol=symbol, orderId=order_id)
            return {"status": "success", "raw": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}
