# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

This project uses `uv` as the Python package manager (Python 3.12 required).

```bash
# Install dependencies
uv sync

# Run the application
uv run python main.py

# Run a specific adapter or module interactively
uv run python -c "from adapters.market_data import CoinLoreMarketDataAdapter; ..."
```

There are no configured test or lint commands — add them via pyproject.toml if needed.

## Environment Variables

Create a `.env` file (gitignored) with:
- `COINDESK_API_KEY` — required by `SecurityMetricsAdapter` and `UrlsAdapter`
- `FIRECRAWL_API_KEY` — required by any adapter using `FirecrawlApp`
- `OPENAI_API_KEY` — required by `ai.py` for GPT-4o-mini calls

## Architecture

The project follows **Hexagonal Architecture (Ports & Adapters)**:

- **`ports/`** — Abstract interfaces (ABCs) and frozen dataclasses (DTOs) that define data contracts. No external API calls here.
- **`adapters/`** — Concrete implementations of ports. Each adapter calls one or more external APIs (CoinLore, CoinGecko, CoinMarketCap, CoinDesk, Alternative.me, DropsTab) and transforms the response into the port's DTO.
- **`indicators/`** — Pure functions that categorize numeric data into enums (e.g., market cap tier, price range, dilution risk). No I/O.
- **`constants/`** — `Asset` and `AssetName` enums for supported cryptocurrencies (BTC, ETH, TRX, SUI, BEAM).
- **`ai.py`** — Calls OpenAI GPT-4o-mini with an aggregated data payload to produce an investment summary.
- **`main.py`** — Orchestrates the full pipeline: instantiate adapters → fetch data → apply indicators → call AI.

### Adding a new data source

1. Define a DTO (frozen dataclass) and an abstract port class in `ports/`.
2. Implement the adapter in `adapters/`, injecting any API clients via the constructor.
3. Export from `ports/__init__.py` and `adapters/__init__.py`.
4. Wire up in `main.py` and pass data to the AI prompt in `ai.py`.

### Adding a new asset

Add entries to `Asset` and `AssetName` in `constants/asset.py`.
