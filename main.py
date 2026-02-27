from fastapi import FastAPI
from app.routes.logbook import router as logbook_router

app = FastAPI(
    title="TrikeTime Logbook API",
    version="0.1.0"
)

from app.db.session import engine
from app.db.base import Base

Base.metadata.create_all(bind=engine)

# подключаем роуты
app.include_router(
    logbook_router,
    prefix="/logbook",
    tags=["Logbook"]
)


@app.get("/")
def root():
    return {"message": "TrikeTime Logbook API is running"}