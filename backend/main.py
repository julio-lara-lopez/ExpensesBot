import os
import re
import sqlite3
from datetime import datetime, timedelta, timezone
from contextlib import closing
from dataclasses import dataclass
from typing import Optional, Tuple, List
from init_db import init_db  # Import the DB initializer

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

# ---------- Config ----------

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_PATH = os.getenv("DB_PATH", "expenses.db")
TZ_OFFSET = int(
    os.getenv("TZ_OFFSET_MINUTES", "-180")
)  # Default: UTC-03:00 (Chile standard approx. adjust as needed)
TAXONOMY = None
def get_taxonomy():
    global TAXONOMY
    if TAXONOMY is None:
        with closing(get_conn()) as conn:
            TAXONOMY = load_taxonomy(conn)
    return TAXONOMY
# ---------- Database ----------


def get_conn():
    # check_same_thread=False so we can use a single connection in async handlers if needed
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn




# ---------- Parsing ----------

amount_re = re.compile(r"(?P<amount>-?\d+(?:[.,]\d{1,2})?)")
# Accepts messages like:
#  "Groceries 25.40"
#  "25.40 groceries milk"
#  "almuerzo 7,5 empanadas"
#  "CLP 3500 comida"
#  "3500 clp pan"
# We will try to detect currency keywords (usd, clp) and normalize comma to dot

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
    # normalize decimal comma
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

    # Split around the amount to infer category vs note
    start, end = m.span()
    left = cleaned[:start].strip()
    right = cleaned[end:].strip()

    # Heuristic: first word in left (if any) is category; else first word in right
    tokens_left = left.split()
    tokens_right = right.split()

    if tokens_left:
        category = tokens_left[0]
        note_tokens = (
            (tokens_left[1:] + tokens_right)
            if (len(tokens_left) > 1 or tokens_right)
            else []
        )
    else:
        category = tokens_right[0] if tokens_right else "misc"
        note_tokens = tokens_right[1:] if len(tokens_right) > 1 else []

    note = " ".join(note_tokens) if note_tokens else None
    return ParsedExpense(
        category=category.capitalize(), amount=amount, note=note, currency=currency
    )


# ---------- Helpers ----------
def load_taxonomy(conn):
    # {category_id: {"name": str, "keywords": [str,...]}}
    cats = {}
    for r in conn.execute("SELECT id, name FROM categories"):
        cats[r["id"]] = {"name": r["name"], "keywords": []}
    for r in conn.execute("""
        SELECT category_id, keyword
        FROM category_keywords
    """):
        cats[r["category_id"]]["keywords"].append(r["keyword"].lower())
    return cats

def classify_category(text: str, cats) -> Optional[tuple]:
    """Return (category_id, category_name) if any keyword matches, else None."""
    t = text.lower()
    best = None
    for cid, info in cats.items():
        for kw in info["keywords"]:
            if kw in t:  # substring match; you can upgrade to token/regex later
                # simple first-hit wins; you could score by longest keyword or count
                return cid, info["name"]
    return best

def now_utc():
    return datetime.now(timezone.utc)


def to_local(dt_utc: datetime) -> datetime:
    return dt_utc + timedelta(minutes=TZ_OFFSET)


def date_range(keyword: str) -> Tuple[datetime, datetime]:
    """Return (start_utc, end_utc) for 'today'/'week'/'month' in local time, converted to UTC boundaries."""
    now_local = to_local(now_utc())
    if keyword == "today":
        start_local = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
        end_local = start_local + timedelta(days=1)
    elif keyword == "week":
        # Start on Monday
        start_local = now_local - timedelta(days=now_local.weekday())
        start_local = start_local.replace(hour=0, minute=0, second=0, microsecond=0)
        end_local = start_local + timedelta(days=7)
    elif keyword == "month":
        start_local = now_local.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        # naive month advance
        if start_local.month == 12:
            end_local = start_local.replace(year=start_local.year + 1, month=1)
        else:
            end_local = start_local.replace(month=start_local.month + 1)
    else:
        # default to today
        start_local = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
        end_local = start_local + timedelta(days=1)

    # convert back to UTC
    start_utc = start_local - timedelta(minutes=TZ_OFFSET)
    end_utc = end_local - timedelta(minutes=TZ_OFFSET)
    return start_utc, end_utc


# ---------- Bot Handlers ----------


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! Send me expenses like:\n"
        "• `Groceries 25.40`\n"
        "• `3500 CLP almuerzo`\n"
        "You can also use /sum today|week|month and /list today|week|month\n"
        "Set env TZ_OFFSET_MINUTES to your local offset (e.g., -180 for UTC-3).",
        parse_mode=ParseMode.MARKDOWN,
    )


async def cmd_sum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    period = context.args[0].lower() if context.args else "today"
    start_utc, end_utc = date_range(period)

    with closing(get_conn()) as conn:
        cur = conn.execute(
            """
            SELECT currency, SUM(amount) as total, COUNT(*) as n
            FROM expenses
            WHERE user_id=? AND ts_utc >= ? AND ts_utc < ?
            GROUP BY currency
            ORDER BY currency;
        """,
            (update.effective_user.id, start_utc.isoformat(), end_utc.isoformat()),
        )
        rows = cur.fetchall()

    if not rows:
        await update.message.reply_text(
            f"No expenses for *{period}*.", parse_mode=ParseMode.MARKDOWN
        )
        return

    lines = [f"*{period.title()}* totals:"]
    for r in rows:
        lines.append(f"- {r['currency']}: {r['total']:.2f} (n={r['n']})")
    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.MARKDOWN)


async def cmd_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    period = context.args[0].lower() if context.args else "today"
    start_utc, end_utc = date_range(period)

    with closing(get_conn()) as conn:
        cur = conn.execute(
            """
            SELECT category, amount, currency, note, ts_utc
            FROM expenses
            WHERE user_id=? AND ts_utc >= ? AND ts_utc < ?
            ORDER BY ts_utc DESC
            LIMIT 50;
        """,
            (update.effective_user.id, start_utc.isoformat(), end_utc.isoformat()),
        )
        rows = cur.fetchall()

    if not rows:
        await update.message.reply_text(
            f"No expenses for *{period}*.", parse_mode=ParseMode.MARKDOWN
        )
        return

    lines = [f"*Last {len(rows)} expenses ({period})*"]
    for r in rows:
        ts_local = to_local(datetime.fromisoformat(r["ts_utc"]))
        ts_str = ts_local.strftime("%Y-%m-%d %H:%M")
        note = f" — _{r['note']}_" if r["note"] else ""
        lines.append(
            f"{ts_str} • {r['category']}: {r['amount']:.2f} {r['currency']}{note}"
        )

    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.MARKDOWN)


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    parsed = parse_expense(update.message.text)
    if not parsed:
        await update.message.reply_text("Use `Categoría Monto [nota]` (ej: `Supermercado 12500`)")
        return

    # Build a “full text” to match keywords (category + note + raw message)
    full_text = " ".join(filter(None, [
        update.message.text, parsed.category, parsed.note
    ]))
    cid_name = classify_category(full_text, get_taxonomy())
    if cid_name:
        category_id, resolved_category = cid_name[0], cid_name[1]
    else:
        category_id = 0
        resolved_category = parsed.category

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id if update.effective_chat else None
    ts_iso = now_utc().isoformat()

    with closing(get_conn()) as conn:
        conn.execute("""
            INSERT INTO expenses (user_id, chat_id, category, category_id, amount, note, currency, ts_utc)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (user_id, chat_id, resolved_category, category_id, parsed.amount, parsed.note, parsed.currency, ts_iso))
        conn.commit()

    await update.message.reply_text(
        f"Added: {resolved_category} {parsed.amount:.2f} {parsed.currency}" + (f" — {parsed.note}" if parsed.note else "")
    )


def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN missing. Set it in .env or environment variables."
        )

    init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("sum", cmd_sum))
    app.add_handler(CommandHandler("list", cmd_list))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
