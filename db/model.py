from os import getenv
from contextlib import contextmanager
from sqlalchemy import String, create_engine, BIGINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from dotenv import load_dotenv

load_dotenv()

ENGINE = getenv('ENGINE')
engine = create_engine(ENGINE, echo=True)


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=True)
    password: Mapped[str] = mapped_column(String(3000), nullable=False)

    def __repr__(self):
        return f"User(user_id={self.user_id}, username={self.username})"


Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
