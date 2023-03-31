from typing import BinaryIO
import gzip

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from server.src.models.role import Role
from server.src.models.user import User
from server.src.routes.auth import router as auth_router
from server.src.routes.games import router as games_router
from server.src.routes.companies import router as companies_router
from server.src.settings import tags_metadata, RoleType, admin_config
from server.src.utils.crypt import get_password_hash
from server.src.utils.db import Base, engine, get_db


def read_in_chunks(file_object: BinaryIO, chunk_size: int) -> bytes:
    while True:
        chunk = file_object.read(chunk_size)
        if not chunk:
            break
        yield chunk


def compress_file(file_path: str, chunk_size: int) -> bytes:
    with open(file_path, "rb") as file:
        for chunk in read_in_chunks(file, chunk_size):
            yield gzip.compress(chunk)


def init_db():
    db = next(get_db())

    _add_roles(db)
    _add_admin(db)


def _add_admin(session):
    admin_role = session.query(Role).filter(Role.title == RoleType.ADMIN).one()

    user = User(
        email=admin_config["EMAIL"],
        account_name=admin_config["ACCOUNT_NAME"],
        displayed_name=admin_config["DISPLAYED_NAME"],
        password=get_password_hash(admin_config["PASSWORD"]),
        is_staff=True,
        is_superuser=True,
        role_id=admin_role.id
    )

    session.add(user)
    session.commit()


def _add_roles(session):
    for role_type in RoleType:
        role = Role(title=role_type)
        session.add(role)
    session.commit()


Base.metadata.create_all(bind=engine)
init_db()

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(auth_router)
app.include_router(games_router)
app.include_router(companies_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/download/")
async def download():
    file_path = "common.rpf"
    chunk_size = 8192
    media_type = "application/gzip"
    headers = {
        "Content-Disposition": f"filename={file_path}"
    }
    return StreamingResponse(
        compress_file(file_path, chunk_size),
        headers=headers,
        media_type=media_type
    )
