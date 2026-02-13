"""Binance account skill — balance, portfolio, account info."""

from binance.client import Client

from makemerich.skills.base import BaseSkill


class AccountSkill(BaseSkill):
    """Get account information from Binance."""

    name = "account"
    description = "Retrieve account balances and portfolio information"

    def __init__(self, config):
        self.client = Client(
            config.binance_api_key,
            config.binance_api_secret,
            testnet=config.mode == "paper",
        )

    async def get_balance(self) -> dict:
        """Get account balance summary."""
        try:
            account = self.client.get_account()
            balances = {
                b["asset"]: {
                    "free": float(b["free"]),
                    "locked": float(b["locked"]),
                }
                for b in account["balances"]
                if float(b["free"]) > 0 or float(b["locked"]) > 0
            }
            return {"status": "success", "balances": balances}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def get_portfolio(self) -> dict:
        """Get full portfolio with current values."""
        try:
            balance = await self.get_balance()
            if balance["status"] == "error":
                return balance

            portfolio = {}
            total_usdt = 0.0

            for asset, amounts in balance["balances"].items():
                total = amounts["free"] + amounts["locked"]
                if asset in ("USDT", "BUSD", "USDC"):
                    usdt_value = total
                else:
                    try:
                        ticker = self.client.get_symbol_ticker(symbol=f"{asset}USDT")
                        usdt_value = total * float(ticker["price"])
                    except Exception:
                        usdt_value = 0.0

                portfolio[asset] = {
                    "amount": total,
                    "usdt_value": round(usdt_value, 2),
                }
                total_usdt += usdt_value

            return {
                "status": "success",
                "portfolio": portfolio,
                "total_usdt": round(total_usdt, 2),
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
