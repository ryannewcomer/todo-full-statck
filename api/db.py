from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional
from pathlib import Path


## HAD TO FIND THE OBSULTE PATH OF THE DATABASE CUS FOR SOME REASON sqlalchemy CANT DETECT IT
DB_FILE = Path(__file__).parent / "database.db"
DB_URL = f"sqlite:///{DB_FILE.as_posix()}"

print(f"THE DATABSE WOULD BE SAVE TO {DB_FILE}")
# databse setup

engine = create_engine(
        DB_URL, echo=True, connect_args={"check_same_thread": False}
)


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(30))


class Tasks(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    desc: Mapped[str]
    dueDays: Mapped[str]
    user_id = mapped_column(ForeignKey("users.id"))


Base.metadata.create_all(engine)
