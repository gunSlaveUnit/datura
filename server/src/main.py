from fastapi import FastAPI
from starlette.responses import JSONResponse

from server.src.settings import DEBUG, Tags
from server.src.utils.db import Base, engine
from server.src.utils.db_init import init_db

app = FastAPI(debug=DEBUG)


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
