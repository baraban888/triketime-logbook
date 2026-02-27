from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./triketime.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # нужно для SQLite в FastAPI
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()