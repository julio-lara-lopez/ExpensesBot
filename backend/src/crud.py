
import os
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone
from typing import Tuple
from src.models import Category, Expense, CategoryKeyword

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db/expenses")
TZ_OFFSET = int(os.getenv("TZ_OFFSET_MINUTES", "-180"))

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def now_utc():
    return datetime.now(timezone.utc)

def to_local(dt_utc: datetime) -> datetime:
    return dt_utc + timedelta(minutes=TZ_OFFSET)

def date_range(keyword: str) -> Tuple[datetime, datetime]:
    now_local = to_local(now_utc())
    if keyword == "today":
        start_local = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
        end_local = start_local + timedelta(days=1)
    elif keyword == "week":
        start_local = now_local - timedelta(days=now_local.weekday())
        start_local = start_local.replace(hour=0, minute=0, second=0, microsecond=0)
        end_local = start_local + timedelta(days=7)
    elif keyword == "month":
        start_local = now_local.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        if start_local.month == 12:
            end_local = start_local.replace(year=start_local.year + 1, month=1)
        else:
            end_local = start_local.replace(month=start_local.month + 1)
    else:
        start_local = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
        end_local = start_local + timedelta(days=1)
    start_utc = start_local - timedelta(minutes=TZ_OFFSET)
    end_utc = end_local - timedelta(minutes=TZ_OFFSET)
    return start_utc, end_utc

def load_taxonomy():
    session = Session()
    cats = {}
    for cat in session.query(Category).all():
        cats[cat.id] = {"name": cat.name, "keywords": []}
    for kw in session.query(CategoryKeyword).all():
        cats[kw.category_id]["keywords"].append(kw.keyword.lower())
    session.close()
    return cats

def add_keyword(category_id: int, keyword: str):
    session = Session()
    kw = CategoryKeyword(category_id=category_id, keyword=keyword.lower())
    session.add(kw)
    session.commit()
    session.close()

def remove_keyword(category_id: int, keyword: str):
    session = Session()
    session.query(CategoryKeyword).filter_by(category_id=category_id, keyword=keyword.lower()).delete()
    session.commit()
    session.close()

def get_keywords_by_category(category_id: int):
    session = Session()
    keywords = session.query(CategoryKeyword.keyword).filter_by(category_id=category_id).all()
    session.close()
    return [kw[0] for kw in keywords]

def list_categories():
    session = Session()
    cats = session.query(Category).all()
    # Include emoji and budget if available in the model
    result = [
        {"id": c.id, "name": c.name, "emoji": c.emoji, "budget": c.budget}
        for c in cats
    ]
    session.close()
    return result

def add_category(name: str, emoji: str = None, budget: float = None):
    session = Session()
    cat = Category(name=name, emoji=emoji, budget=budget)
    session.add(cat)
    session.commit()
    session.close()

def set_budget(category_id: int, amount: float):
    session = Session()
    cat = session.query(Category).filter_by(id=category_id).first()
    if cat:
        cat.budget = amount
        session.commit()
    session.close()

def remove_category(category_id: int):
    session = Session()
    session.query(Category).filter_by(id=category_id).delete()
    session.commit()
    session.close()

def get_expenses(user_id: int, period: str):
    start_utc, end_utc = date_range(period)
    session = Session()
    expenses = session.query(Expense).filter(
        Expense.user_id == user_id,
        Expense.ts_utc >= start_utc.isoformat(),
        Expense.ts_utc < end_utc.isoformat()
    ).order_by(Expense.ts_utc.desc()).limit(50).all()
    result = [
        {
            "category": e.category,
            "amount": e.amount,
            "currency": e.currency,
            "note": e.note,
            "ts_utc": e.ts_utc
        }
        for e in expenses
    ]
    session.close()
    return result

def get_summary(user_id: int, period: str):
    start_utc, end_utc = date_range(period)
    session = Session()
    summary = session.query(
        Expense.currency,
        func.sum(Expense.amount).label("total"),
        func.count(Expense.id).label("n")
    ).filter(
        Expense.user_id == user_id,
        Expense.ts_utc >= start_utc.isoformat(),
        Expense.ts_utc < end_utc.isoformat()
    ).group_by(Expense.currency).order_by(Expense.currency).all()
    result = [
        {
            "currency": s.currency,
            "total": float(s.total),
            "n": s.n
        }
        for s in summary
    ]
    session.close()
    return result

def add_expense(user_id: int, category_id: int, amount: float, date, description: str = None):
    session = Session()
    expense = Expense(
        category_id=category_id,
        amount=amount,
        date=date,
        description=description,
    )
    session.add(expense)
    session.commit()
    session.close()
