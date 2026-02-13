"""Market data skill — prices, klines, order book from Binance."""

from binance.client import Client

from makemerich.skills.base import BaseSkill


class MarketDataSkill(BaseSkill):
    """Fetch market data from Binance."""

    name = "market_data"
    description = "Retrieve market data: prices, klines, order book"

    def __init__(self, config):
        self.client = Client(
            config.binance_api_key,
            config.binance_api_secret,
            testnet=config.mode == "paper",
        )

    async def get_price(self, symbol: str) -> dict:
        """Get current price for a symbol."""
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return {"status": "success", "symbol": symbol, "price": float(ticker["price"])}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def get_klines(self, symbol: str, interval: str = "1h",
                         limit: int = 100) -> list:
        """Get candlestick/kline data."""
        try:
            klines = self.client.get_klines(
                symbol=symbol,
                interval=interval,
                limit=limit,
            )
            return [
                {
                    "timestamp": k[0],
                    "open": float(k[1]),
                    "high": float(k[2]),
                    "low": float(k[3]),
                    "close": float(k[4]),
                    "volume": float(k[5]),
                    "close_time": k[6],
                    "quote_volume": float(k[7]),
                    "trades": k[8],
                }
                for k in klines
            ]
        except Exception as e:
            return []

    async def get_order_book(self, symbol: str, limit: int = 20) -> dict:
        """Get order book depth."""
        try:
            depth = self.client.get_order_book(symbol=symbol, limit=limit)
            return {
                "status": "success",
                "bids": [[float(p), float(q)] for p, q in depth["bids"]],
                "asks": [[float(p), float(q)] for p, q in depth["asks"]],
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def get_24h_stats(self, symbol: str) -> dict:
        """Get 24h statistics for a symbol."""
        try:
            stats = self.client.get_ticker(symbol=symbol)
            return {
                "status": "success",
                "symbol": symbol,
                "price_change_pct": float(stats["priceChangePercent"]),
                "high": float(stats["highPrice"]),
                "low": float(stats["lowPrice"]),
                "volume": float(stats["volume"]),
                "quote_volume": float(stats["quoteVolume"]),
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
