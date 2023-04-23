import redis as redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from server.src.core.settings import CONNECTION_STRING, redis_config

engine = create_engine(CONNECTION_STRING)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


def get_session_storage():
    storage = redis.Redis(
        host=redis_config["HOST"],
        port=int(redis_config["PORT"]),
        db=redis_config["DB"]
    )
    try:
        yield storage
    finally:
        storage.quit()
