"""
FastAPI Checkers AI
"""
import sys

from fastapi import FastAPI
from app.models.checkers_models import CheckersRequest
from app.checkers.node import Node
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
    # root = Node(board=request.board, player=False)
    # root.can_jump = root.find_jump()
    # moves = root.get_all_valid_moves()
    # print("Moves: ", moves)
    return {"moves": service.get_best_move(request.board)}
