from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src import crud

router = APIRouter(tags=["Expenses"])

class Expense(BaseModel):
    user_id: int
    text: str

@router.get("", tags=["Expenses"])
def list_expenses(period: str = "today", user_id: int = 0):
    return crud.get_expenses(user_id, period)

@router.get("/summary", tags=["Expenses"])
def get_summary(period: str = "today", user_id: int = 0):
    return crud.get_summary(user_id, period)

@router.post("", tags=["Expenses"])
def add_expense(expense: Expense):
    try:
        import re
        from datetime import date
        amount_re = re.compile(r"(?P<amount>-?\d+(?:[.,]\d{1,2})?)")
        cleaned = expense.text.replace(",", ".")
        m = amount_re.search(cleaned)
        if not m:
            raise HTTPException(status_code=400, detail="Could not parse amount from text.")
        amount_str = m.group("amount")
        try:
            amount = float(amount_str)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid amount format.")
        start, end = m.span()
        left = cleaned[:start].strip()
        right = cleaned[end:].strip()
        text_without_amount = f"{left} {right}".strip().lower()
        cats = crud.load_taxonomy()
        matched_id = None
        matched_keyword = None
        for cid, info in cats.items():
            for kw in info["keywords"]:
                kw_lower = kw.lower()
                pattern = r"\b" + re.escape(kw_lower) + r"\b"
                if re.search(pattern, text_without_amount):
                    matched_id = cid
                    matched_keyword = kw_lower
                    break
            if matched_id:
                break
        if matched_id:
            note = re.sub(r"\b" + re.escape(matched_keyword) + r"\b", "", text_without_amount).strip() or None
        else:
            tokens_left = left.split()
            tokens_right = right.split()
            if tokens_left:
                category_candidate = tokens_left[0]
                note_tokens = (tokens_left[1:] + tokens_right) if (len(tokens_left) > 1 or tokens_right) else []
            else:
                category_candidate = tokens_right[0] if tokens_right else "misc"
                note_tokens = tokens_right[1:] if len(tokens_right) > 1 else []
            note = " ".join(note_tokens) if note_tokens else None
            category_candidate_lower = category_candidate.lower()
            for cid, info in cats.items():
                if category_candidate_lower == info["name"].lower() or category_candidate_lower in info["keywords"]:
                    matched_id = cid
                    break
            if not matched_id:
                raise HTTPException(status_code=400, detail=f"Category not found for '{category_candidate}'")
        # Insert expense with DB fields
        crud.add_expense(
            user_id=expense.user_id,
            category_id=matched_id,
            amount=amount,
            date=date.today(),
            description=note or expense.text,
        )
        cat_info = cats.get(matched_id, {})
        return {
            "status": "success",
            "message": "Expense added.",
            "category": cat_info.get("name"),
            "emoji": cat_info.get("emoji"),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
