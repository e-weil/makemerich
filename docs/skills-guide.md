# Skills Guide

Skills are modular adapters that connect MakeMeRich to exchanges and analysis tools.

## Creating a New Exchange Skill

1. Create a directory under `makemerich/skills/`:
```
makemerich/skills/coinbase/
├── __init__.py
├── spot.py
├── account.py
└── market_data.py
```

2. Extend `BaseSkill`:
```python
from makemerich.skills.base import BaseSkill

class CoinbaseSpotSkill(BaseSkill):
    name = "coinbase_spot"
    description = "Execute spot trades on Coinbase"

    async def buy(self, symbol, amount_usdt, order_type="market", limit_price=None):
        # Implement exchange-specific logic
        ...

    async def sell(self, symbol, amount, order_type="market", limit_price=None):
        ...
```

3. Register the skill in `engine.py`

## Existing Skills

- **Binance Spot** — `skills/binance/spot.py`
- **Binance Futures** — `skills/binance/futures.py`
- **Binance Account** — `skills/binance/account.py`
- **Market Data** — `skills/binance/market_data.py`
- **Technical Analysis** — `skills/analysis/technical.py`
- **Sentiment Analysis** — `skills/analysis/sentiment.py`
- **Pattern Detection** — `skills/analysis/patterns.py`
