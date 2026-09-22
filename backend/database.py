import os
from pathlib import Path
from sqlalchemy import event
from sqlmodel import SQLModel, Session, create_engine

database_url = os.getenv("DATABASE_URL", "sqlite:///" + str(Path(__file__).with_name("shop.db")))
engine = create_engine(database_url, connect_args={"check_same_thread": False, "timeout": 20})


@event.listens_for(engine, "connect")
def enable_foreign_keys(connection, record):
    connection.execute("PRAGMA foreign_keys=ON")


def get_session():
    with Session(engine) as session:
        yield session


def create_tables():
    SQLModel.metadata.create_all(engine)
