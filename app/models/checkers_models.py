"""
Checkers API Request Models
"""
from typing import List
from pydantic import BaseModel

class CheckersRequest(BaseModel):
    """
    Checkers AI Request Model
    """
    board: List[List[int]]
