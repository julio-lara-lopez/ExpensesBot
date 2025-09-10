import os
import sys
import types

import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class _APIRouter:
    def __init__(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        def decorator(func):
            return func

        return decorator

    def post(self, *args, **kwargs):
        def decorator(func):
            return func

        return decorator


class _HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class _BaseModel:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


sys.modules.setdefault("fastapi", types.SimpleNamespace(APIRouter=_APIRouter, HTTPException=_HTTPException))
sys.modules.setdefault("pydantic", types.SimpleNamespace(BaseModel=_BaseModel))
crud_stub = types.ModuleType("crud")
crud_stub.load_taxonomy = lambda: {}
crud_stub.add_expense = lambda **kwargs: None
sys.modules.setdefault("src.crud", crud_stub)

from src.api import expenses


def setup_taxonomy(monkeypatch):
    taxonomy = {
        1: {"name": "Transporte", "emoji": "", "keywords": ["uber"]},
        2: {"name": "Comida Afuera", "emoji": "", "keywords": ["uber eats"]},
    }
    monkeypatch.setattr(expenses.crud, "load_taxonomy", lambda: taxonomy)
    recorded = {}

    def fake_add_expense(**kwargs):
        recorded["category_id"] = kwargs["category_id"]

    monkeypatch.setattr(expenses.crud, "add_expense", fake_add_expense)
    return recorded


def test_uber_maps_to_transporte(monkeypatch):
    recorded = setup_taxonomy(monkeypatch)
    expense = expenses.Expense(user_id=1, text="uber 10")
    result = expenses.add_expense(expense)
    assert recorded["category_id"] == 1
    assert result["category"] == "Transporte"


def test_uber_eats_maps_to_comida_afuera(monkeypatch):
    recorded = setup_taxonomy(monkeypatch)
    expense = expenses.Expense(user_id=1, text="uber eats 15")
    result = expenses.add_expense(expense)
    assert recorded["category_id"] == 2
    assert result["category"] == "Comida Afuera"
