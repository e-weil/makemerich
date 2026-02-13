# Getting Started

## Prerequisites

- Python 3.10+
- Binance account (with API keys)
- Anthropic API key (for Claude)

## Installation

```bash
git clone https://github.com/e-weil/makemerich.git
cd makemerich
pip install -r requirements.txt
```

## Configuration

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` with your API keys:
- `BINANCE_API_KEY` / `BINANCE_API_SECRET` — from Binance API management
- `ANTHROPIC_API_KEY` — from console.anthropic.com

3. Review `config/default.yaml` for trading parameters

## First Run (Paper Trading)

Always start with paper trading:

```bash
python -m makemerich.main --mode paper --pairs BTCUSDT ETHUSDT
```

This uses Binance testnet — no real money involved.

## Going Live

Once you're confident in your setup:

```bash
python -m makemerich.main --mode live --pairs BTCUSDT
```

**Warning:** Live mode uses real money. Start small.
