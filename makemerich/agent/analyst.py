"""Market analyst agent — provides market analysis context to the trader."""

from makemerich.core.logger import get_logger


class MarketAnalyst:
    """Analyzes market conditions and provides context for trading decisions."""

    def __init__(self, config, skills):
        self.config = config
        self.skills = skills
        self.logger = get_logger("analyst")

    async def analyze(self, pairs: list) -> dict:
        """Run full analysis on the given trading pairs."""
        results = {}
        for pair in pairs:
            results[pair] = await self._analyze_pair(pair)
        return results

    async def _analyze_pair(self, pair: str) -> dict:
        """Analyze a single trading pair."""
        market_data = await self.skills["market_data"].get_klines(
            symbol=pair,
            interval=self.config.timeframe,
            limit=100,
        )

        technical = self.skills["technical"].analyze(market_data)

        return {
            "pair": pair,
            "technical": technical,
            "market_data": market_data,
        }
