from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.api.categories import router as categories_router
from src.api.expenses import router as expenses_router

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
