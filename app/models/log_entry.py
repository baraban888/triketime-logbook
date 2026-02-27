from datetime import date, time
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class LogEntry(Base):
    __tablename__ = "log_entries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # ключевая дата записи
    day: Mapped[date] = mapped_column(index=True)

    start_time: Mapped[time]
    start_place: Mapped[str]

    end_time: Mapped[time]
    end_place: Mapped[str]

    km: Mapped[int | None] = mapped_column(nullable=True)
    note: Mapped[str | None] = mapped_column(nullable=True)