import logging

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.api.categories import router as categories_router
from src.api.expenses import router as expenses_router
from src import crud

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories_router, prefix="/categories")
app.include_router(expenses_router, prefix="/expenses")


@app.on_event("startup")
def init_db_connection():
    """Establish and immediately dispose of a database connection."""
    logger = logging.getLogger(__name__)
    try:
        conn = crud.engine.connect()
        conn.close()
        crud.engine.dispose()
    except Exception:
        logger.exception("Failed to establish initial database connection")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
