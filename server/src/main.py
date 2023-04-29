from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from server.src.core.utils.db import Base, engine
from server.src.core.utils.db_init import init_db
from server.src.core.settings import DEBUG, Tags
from server.src.api.v1.api import router as api_v1_router
from server.src.admin.api import router as admin_router

app = FastAPI(debug=DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)
app.include_router(admin_router)


@app.on_event("startup")
async def startup_event() -> None:
    """
    Creating models and calling the database initializer at application startup
    """

    Base.metadata.create_all(bind=engine)
    init_db()


@app.get("/", tags=[Tags.HOME])
async def api_information() -> JSONResponse:
    """
    Information about the current versions of the service API
    """

    return JSONResponse({
        "title": "Foggie API",
        "purpose": "Online service for digital distribution of computer games and programs",
        "api": [
            {
                "version": "1",
                "status": "development",
                "description": ""
            }
        ]
    })
