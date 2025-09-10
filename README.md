# Telegram Expense Bot (Dev Mode, SQLite)

A minimal Telegram bot to log expenses into a local SQLite database.

## Features
- Send messages like `Groceries 25.40 milk` or `3500 CLP comida`
- Auto-detects amount and (rudimentary) currency (USD/CLP)
- Commands:
  - `/start` — quick help
  - `/sum [today|week|month]` — totals by currency
  - `/list [today|week|month]` — last 50 entries within period
  - `/chatid` — reply with your chat ID for reminder configuration

## Quickstart

1. **Create a bot** via [@BotFather](https://t.me/BotFather) and copy the token.
2. **Clone or unzip this project**.
3. **Setup Python env** (3.10+ recommended) and install deps:
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure environment**:
   - Copy `.env.example` to `.env`
   - Set `BOT_TOKEN=...`
   - Optionally adjust `TZ_OFFSET_MINUTES` for your local time (e.g., -180 for UTC-3).
5. **Run**:
   ```sh
   python main.py
   ```
6. **Use it**: text the bot like `Groceries 25.40 milk`.

## Notes
- Database file defaults to `expenses.db` in the project directory.
- Schema is created automatically on first run.
- Parsing is tolerant to `,` or `.` decimals and basic CLP/USD cues.
- For dev, this is single-process and uses SQLite. For production, consider PostgreSQL and webhooks.

## Examples
- `Groceries 25.40` → category=Groceries, amount=25.40, currency=USD
- `3500 CLP pan` → category=Pan, amount=3500.00, currency=CLP
- `almuerzo 7,5 empanadas` → category=Almuerzo, amount=7.50, note="empanadas"

## Troubleshooting
- If you see `BOT_TOKEN missing`, ensure `.env` is created and filled.
- If messages aren't received, verify the bot is started (send `/start`) and the token is correct.
- Set `TZ_OFFSET_MINUTES` to match your local zone for correct daily/weekly/monthly rollups.