# CLAUDE.md — MakeMeRich

## The MakeMeRich Six

| # | Name | Role |
|---|------|------|
| 0 | Ivan | The Spark — founder |
| 1 | ATLAS | El Arquitecto — data & calculations |
| 2 | NOVA | La Creativa — UI/UX design |
| 3 | CIPHER | El Ingeniero — app logic |
| 4 | PULSE | El Estratega — viral growth |
| 5 | FORGE | El Constructor — infrastructure |

## What is MakeMeRich?

A viral web app that shows people their global wealth ranking.
Enter your income → see where you stand on planet Earth.

**No AI. No tokens. No backend required. Pure HTML + CSS + JS.**

## Quick Start

```bash
# Option 1: Just open the file
open app/index.html

# Option 2: Serve with Python
cd app && python -m http.server 8080

# Option 3: Serve with FastAPI
pip install fastapi uvicorn
uvicorn app.api.app:app --reload

# Option 4: Docker
docker compose up
```

## Project Structure

```
app/
├── index.html          # Single page app (NOVA)
├── css/style.css       # Styling (NOVA)
├── js/
│   ├── calculator.js   # Wealth calculations (ATLAS)
│   ├── app.js          # Main controller (CIPHER)
│   ├── rankings.js     # Ranking utilities (CIPHER)
│   ├── comparisons.js  # Billionaire comparisons (CIPHER)
│   ├── cards.js        # Wealth Card generator (PULSE)
│   └── share.js        # Social sharing (PULSE)
├── data/
│   ├── countries.json  # Income by country (ATLAS)
│   ├── billionaires.json # Top billionaires (ATLAS)
│   └── tips.json       # Daily money tips (ATLAS)
├── api/
│   └── app.py          # FastAPI server (FORGE)
└── assets/
    └── img/

trading-bot-v1 branch   # Original crypto trading bot (preserved)
```

## Git Rules

- Author: `E. Weil <weil@doli.network>`
- No AI-related co-author annotations
