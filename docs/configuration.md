# Configuration

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BINANCE_API_KEY` | Binance API key | Yes |
| `BINANCE_API_SECRET` | Binance API secret | Yes |
| `ANTHROPIC_API_KEY` | Anthropic API key | Yes |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | No |
| `TELEGRAM_CHAT_ID` | Telegram chat ID | No |

## YAML Configuration

### `config/default.yaml`

- `mode`: `paper` (testnet) or `live` (real money)
- `cycle_interval`: Seconds between analysis cycles
- `timeframe`: Candlestick timeframe (1m, 5m, 15m, 1h, 4h, 1d)
- `trading_pairs`: List of pairs to trade

### Risk Settings

- `max_risk_per_trade`: Maximum % of portfolio to risk per trade
- `max_positions`: Maximum concurrent open positions
- `min_cash_percent`: Minimum % to keep in stablecoins
- `max_leverage`: Maximum leverage (1 = no leverage)
- `default_stop_loss_pct`: Default stop-loss percentage

### Strategy Presets

- `config/strategies/conservative.yaml` — Low risk, major pairs only
- `config/strategies/aggressive.yaml` — Higher risk/reward, more pairs
- `config/strategies/scalper.yaml` — Frequent small trades
