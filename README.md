# MakeMeRich

**The AI that actually makes you money.**

Open-source autonomous crypto trading agent. Connects AI to your Binance
account and trades for you. Transparent. Local. Yours.

## What is this?

MakeMeRich is to trading what [OpenClaw](https://github.com/openclaw/openclaw)
is to personal assistance. OpenClaw connects an LLM to your messaging apps
and does things for you. MakeMeRich connects an LLM to your exchange
and trades for you.

- **AI-Powered** — Claude analyzes markets and makes trading decisions
- **CrystalBox** — Every trade has a full reasoning chain. No black boxes.
- **Local-First** — Runs on your machine. Your keys, your data, your money
- **Skill-Based** — Modular architecture. Add exchanges, strategies, signals
- **Paper Trading** — Test strategies with fake money before going live
- **Open Source** — MIT License. Fork it, modify it, make it yours

## Quick Start

```bash
git clone https://github.com/e-weil/makemerich.git
cd makemerich
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys

# Paper trading (safe, no real money)
python -m makemerich.main --mode paper --pairs BTCUSDT ETHUSDT

# Live trading (real money — use at your own risk)
python -m makemerich.main --mode live --pairs BTCUSDT
```

## Architecture

```
┌──────────────────────────────────────────────────┐
│                  MakeMeRich Engine                │
├──────────┬───────────┬───────────┬───────────────┤
│  Agent   │  Skills   │ CrystalBox│   Channels    │
│ (LLM     │ (Binance, │ (Audit,   │  (Telegram,   │
│  brain)  │  Analysis)│  Reason)  │   Discord)    │
└──────────┴───────────┴───────────┴───────────────┘
```

### Components

- **Engine** (`core/engine.py`) — The heart. Orchestrates analysis cycles, connects skills to the agent.
- **Agent** (`agent/trader.py`) — The brain. Uses Claude to analyze markets and decide trades.
- **Skills** (`skills/`) — Exchange adapters (Binance spot/futures) and analysis tools (RSI, MACD, patterns).
- **CrystalBox** (`crystalbox/`) — Transparency layer. Every decision logged with full reasoning chain and tamper-evident hashing.
- **Strategies** (`strategies/`) — Pre-built strategies: momentum, mean reversion, grid, smart DCA.
- **Channels** (`channels/`) — Notifications via Telegram, Discord, or webhooks.

## Configuration

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Edit `config/default.yaml` to customize trading parameters, or use a pre-built strategy:

```bash
# Conservative (low risk)
python -m makemerich.main --config config/strategies/conservative.yaml

# Aggressive (higher risk/reward)
python -m makemerich.main --config config/strategies/aggressive.yaml
```

## CrystalBox — Transparency

Every trading decision is logged with:
- Full reasoning chain from the AI
- Technical indicators at time of decision
- Confidence level
- Tamper-evident hash chain (like a mini-blockchain)

View the audit log:
```bash
# Start the dashboard
uvicorn makemerich.web.app:app --reload

# Or check the raw log
cat data/crystalbox/audit.jsonl | python -m json.tool
```

## Disclaimer

This is experimental software. Trading cryptocurrency involves substantial
risk of loss. MakeMeRich is open source — you run it, you configure it,
you are responsible for your own trades. The authors are not responsible
for any financial losses. Start with paper trading. Always.

## License

MIT
