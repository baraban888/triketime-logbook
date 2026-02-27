from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from app.models.log_entry import LogEntry
from app.schemas.log_entry import LogEntryCreate, LogEntryUpdate


class LogbookService:
    def __init__(self, db: Session):
        self.db = db

    def create_entry(self, payload: LogEntryCreate) -> LogEntry:
        entry = LogEntry(**payload.model_dump())
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def list_entries(
        self,
        day_from: date | None,
        day_to: date | None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[LogEntry]:
        stmt = select(LogEntry)

        conditions = []
        if day_from is not None:
            conditions.append(LogEntry.day >= day_from)
        if day_to is not None:
            conditions.append(LogEntry.day <= day_to)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = (
            stmt.order_by(LogEntry.day.desc(), LogEntry.start_time.desc(), LogEntry.id.desc())
            .limit(limit)
            .offset(offset)
        )

        return list(self.db.scalars(stmt))

    def get_entry(self, entry_id: int) -> LogEntry:
        entry = self.db.get(LogEntry, entry_id)
        if not entry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log entry not found")
        return entry

    def update_entry(self, entry_id: int, payload: LogEntryUpdate) -> LogEntry:
        entry = self.get_entry(entry_id)

        data = payload.model_dump(exclude_unset=True)
        if not data:
            return entry  # ничего не меняем

        for key, value in data.items():
            setattr(entry, key, value)

        self.db.commit()
        self.db.refresh(entry)
        return entry

    def delete_entry(self, entry_id: int) -> None:
        entry = self.get_entry(entry_id)
        self.db.delete(entry)
        self.db.commit()