from fastapi import FastAPI
from src.db import models
from src.db.database import engine
from src.router.currency import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/ping/")
async def ping():
    return {"message": "pong"}

app.include_router(router)