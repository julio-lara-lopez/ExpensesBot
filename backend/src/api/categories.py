from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from src import crud

router = APIRouter(tags=["Categories"])

class Keyword(BaseModel):
    keyword: str

class Category(BaseModel):
    name: str
    emoji: Optional[str] = None
    budget: Optional[float] = None

@router.post("", tags=["Categories"])
def add_category(category: Category):
    try:
        crud.add_category(category.name, category.emoji, category.budget)
        return {"status": "success", "message": f"Category '{category.name}' added."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{category_id}", tags=["Categories"])
def remove_category(category_id: int):
    try:
        crud.remove_category(category_id)
        return {"status": "success", "message": f"Category with id {category_id} removed."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", tags=["Categories"])
def list_categories():
    return crud.list_categories()


@router.get("/budget-status", tags=["Categories"])
def get_budget_status():
    return crud.get_budget_status()


class Budget(BaseModel):
    budget: float


@router.put("/{category_id}/budget", tags=["Categories"])
def set_budget(category_id: int, payload: Budget):
    try:
        crud.set_budget(category_id, payload.budget)
        return {
            "status": "success",
            "message": f"Budget for category {category_id} set to {payload.budget}.",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{category_id}/keywords", tags=["Categories"])
def get_keywords_by_category(category_id: int):
    return crud.get_keywords_by_category(category_id)

@router.post("/{category_id}/keywords", tags=["Categories"])
def add_keyword_to_category(category_id: int, keyword: Keyword):
    try:
        crud.add_keyword(category_id, keyword.keyword)
        return {"status": "success", "message": f"Keyword '{keyword.keyword}' added to category {category_id}."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{category_id}/keywords", tags=["Categories"])
def remove_keyword_from_category(category_id: int, keyword: Keyword):
    try:
        crud.remove_keyword(category_id, keyword.keyword)
        return {"status": "success", "message": f"Keyword '{keyword.keyword}' removed from category {category_id}."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
