# Strategies Guide

## Built-in Strategies

### Momentum
Rides the trend. Buys when momentum is building (RSI recovering from oversold + MACD bullish), sells when momentum fades.

### Mean Reversion
Buys when price hits the lower Bollinger Band with oversold RSI, sells at the upper band. Works best in ranging markets.

### Grid Trading
Places buy and sell orders at regular price intervals. Profits from price oscillation within a defined range.

### Smart DCA
Dollar Cost Averaging with intelligence. Buys at regular intervals but increases position size during significant dips.

## Creating a New Strategy

1. Create a file in `makemerich/strategies/`
2. Extend `BaseStrategy`:

```python
from makemerich.strategies.base import BaseStrategy, Signal

class MyStrategy(BaseStrategy):
    name = "my_strategy"

    def evaluate(self, analysis: dict, portfolio: dict) -> Signal:
        # Your logic here
        return Signal(
            action="BUY",  # BUY, SELL, or HOLD
            pair="BTCUSDT",
            strength=0.8,
            reason="My reasoning",
            stop_loss=49000,
            take_profit=55000,
        )
```
