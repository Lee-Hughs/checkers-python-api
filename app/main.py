"""
FastAPI Checkers AI
"""
from fastapi import FastAPI
from app.models.checkers_models import CheckersRequest
from app.checkers import service

app = FastAPI()

@app.get("/")
async def root():
    """
    Root Router
    """
    return {"message": "Hello World"}

@app.post("/checkers")
async def checkers(request: CheckersRequest):
    """
    Get Checkers Move
    """
    return {"moves": service.get_best_move(request.board)}
