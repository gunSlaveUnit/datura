from fastapi import FastAPI

from server.src.routes.auth import router as auth_router
from server.src.routes.games import router as games_router
from server.src.routes.companies import router as companies_router
from server.src.routes.library import router as library_router
from server.src.routes.users import router as users_router
from server.src.routes.cart import router as cart_router
from server.src.settings import tags_metadata
from server.src.utils.db import Base, engine
from server.src.utils.db_init import init_db


app = FastAPI(openapi_tags=tags_metadata)

app.include_router(auth_router)
app.include_router(games_router)
app.include_router(companies_router)
app.include_router(library_router)
app.include_router(users_router)
app.include_router(cart_router)


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    init_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}
