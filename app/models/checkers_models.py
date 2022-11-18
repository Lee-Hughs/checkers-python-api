from pydantic import BaseModel
from typing import List

class CheckersRequest(BaseModel):
    board: List[List[int]]