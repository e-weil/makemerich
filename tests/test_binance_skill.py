"""Tests for Binance skills (mocked — no real API calls)."""

import pytest
from unittest.mock import MagicMock, patch
from makemerich.core.config import Config


class TestSpotTradingSkill:
    @patch("makemerich.skills.binance.spot.Client")
    def test_buy_market_order(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.order_market_buy.return_value = {
            "orderId": 12345,
            "executedQty": "0.001",
            "fills": [{"price": "50000.00"}],
        }
        mock_client_cls.return_value = mock_client

        from makemerich.skills.binance.spot import SpotTradingSkill
        config = Config()
        skill = SpotTradingSkill(config)

        import asyncio
        result = asyncio.run(skill.buy("BTCUSDT", 100, "market"))

        assert result["status"] == "success"
        assert result["order_id"] == 12345
        assert result["side"] == "BUY"

    @patch("makemerich.skills.binance.spot.Client")
    def test_sell_market_order(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.order_market_sell.return_value = {
            "orderId": 12346,
            "executedQty": "0.001",
            "fills": [{"price": "51000.00"}],
        }
        mock_client_cls.return_value = mock_client

        from makemerich.skills.binance.spot import SpotTradingSkill
        config = Config()
        skill = SpotTradingSkill(config)

        import asyncio
        result = asyncio.run(skill.sell("BTCUSDT", 0.001, "market"))

        assert result["status"] == "success"
        assert result["side"] == "SELL"

    @patch("makemerich.skills.binance.spot.Client")
    def test_buy_error_handling(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.order_market_buy.side_effect = Exception("API Error")
        mock_client_cls.return_value = mock_client

        from makemerich.skills.binance.spot import SpotTradingSkill
        config = Config()
        skill = SpotTradingSkill(config)

        import asyncio
        result = asyncio.run(skill.buy("BTCUSDT", 100, "market"))

        assert result["status"] == "error"
        assert "API Error" in result["message"]
