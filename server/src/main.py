from fastapi import FastAPI

from server.src.settings import DEBUG
from server.src.utils.db import Base, engine
from server.src.utils.db_init import init_db


app = FastAPI(debug=DEBUG)


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    init_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}
