import os
import re
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Optional
from init_db import init_db

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import httpx
import logging

# ---------- Config ----------

# ---------- Logging ----------
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("API_BASE_URL", "http://backend:8000")



# ---------- Parsing ----------

amount_re = re.compile(r"(?P<amount>-?\d+(?:[.,]\d{1,2})?)")
CURRENCY_ALIASES = {
    "clp": ["clp", "pesos", "peso", "$clp", "ch$", "chil", "cl"],
    "usd": ["usd", "us$", "dolar", "dólar", "$usd", "u$s", "dolares", "dólares", "$"],
}

def detect_currency(text: str) -> str:
    t = text.lower()
    for code, variants in CURRENCY_ALIASES.items():
        for v in variants:
            if f" {v} " in f" {t} ":
                return code.upper()
    return "CLP"

@dataclass
class ParsedExpense:
    category: str
    amount: float
    note: Optional[str]
    currency: str

def parse_expense(text: str) -> Optional[ParsedExpense]:
    cleaned = text.replace(",", ".")
    m = amount_re.search(cleaned)
    if not m:
        return None

    amount_str = m.group("amount")
    try:
        amount = float(amount_str)
    except ValueError:
        return None

    currency = detect_currency(cleaned)
    start, end = m.span()
    left = cleaned[:start].strip()
    right = cleaned[end:].strip()

    tokens_left = left.split()
    tokens_right = right.split()

    if tokens_left:
        category = tokens_left[0]
        note_tokens = (tokens_left[1:] + tokens_right) if (len(tokens_left) > 1 or tokens_right) else []
    else:
        category = tokens_right[0] if tokens_right else "misc"
        note_tokens = tokens_right[1:] if len(tokens_right) > 1 else []

    note = " ".join(note_tokens) if note_tokens else None
    return ParsedExpense(
        category=category.capitalize(), amount=amount, note=note, currency=currency
    )

# ---------- Helpers ----------

def classify_category(text: str, cats) -> Optional[tuple]:
    t = text.lower()
    for cid, info in cats.items():
        for kw in info["keywords"]:
            if kw in t:
                return cid, info["name"]
    return None

# ---------- Bot Handlers ----------

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hola! Puedes enviar tus gastos con el siguiente formato:\n"
        "• `Unimarc 25.40`\n"
        "• `3500 CLP almuerzo`\n"
        "También puedes usar /sum today|week|month y /list today|week|month",
        parse_mode=ParseMode.MARKDOWN,
    )

async def cmd_sum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    period = context.args[0].lower() if context.args else "today"
    user_id = update.effective_user.id
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/expenses/summary", params={"period": period, "user_id": user_id})
        rows = resp.json()
    if not rows:
        await update.message.reply_text(f"No expenses for *{period}*.", parse_mode=ParseMode.MARKDOWN)
        return
    lines = [f"*{period.title()}* totals:"]
    for r in rows:
        lines.append(f"- {r['currency']}: {r['total']:.2f} (n={r['n']})")
    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.MARKDOWN)

async def cmd_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    period = context.args[0].lower() if context.args else "today"
    user_id = update.effective_user.id
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/expenses", params={"period": period, "user_id": user_id})
        rows = resp.json()
    if not rows:
        await update.message.reply_text(f"No expenses for *{period}*.", parse_mode=ParseMode.MARKDOWN)
        return
    lines = [f"*Last {len(rows)} expenses ({period})*"]
    for r in rows:
        ts_local = datetime.fromisoformat(r["ts_utc"]) + timedelta(minutes=-180)  # TODO: get tz offset from API
        ts_str = ts_local.strftime("%Y-%m-%d %H:%M")
        note = f" — _{r['note']}" if r["note"] else ""
        lines.append(f"{ts_str} • {r['category']}: {r['amount']:.2f} {r['currency']}{note}")
    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.MARKDOWN)

async def cmd_chatid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return the chat ID so the user can configure reminders."""
    await update.message.reply_text(str(update.effective_chat.id))

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    user_id = update.effective_user.id
    payload = {
        "user_id": user_id,
        "text": update.message.text,
    }
    logging.info(f"Payload to /expenses: {payload}")
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/expenses", json=payload)
        result = resp.json()
    if resp.status_code == 200:
        category = result.get("category")
        emoji = result.get("emoji") or ""
        if category:
            msg = f"Expense added to {category} {emoji}".strip()
        else:
            msg = "Expense added."
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text(f"Error: {result.get('detail', 'Unknown error')}")



def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN missing. Set it in .env or environment variables.")


    init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("sum", cmd_sum))
    app.add_handler(CommandHandler("list", cmd_list))
    app.add_handler(CommandHandler("chatid", cmd_chatid))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
