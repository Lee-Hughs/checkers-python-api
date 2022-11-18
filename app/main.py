from fastapi import FastAPI
from app.models.checkers_models import CheckersRequest

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/checkers")
async def checkers(request: CheckersRequest):
    return {"moves": [[0,0], [1,1]]}