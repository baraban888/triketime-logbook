from datetime import date
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.log_entry import (
    LogEntryCreate,
    LogEntryRead,
    LogEntryUpdate,
)
from app.services.logbook_service import LogbookService

router = APIRouter()


@router.post(
    "/entries",
    response_model=LogEntryRead,
    status_code=status.HTTP_201_CREATED,
)
def create_entry(payload: LogEntryCreate, db: Session = Depends(get_db)):
    """
    Create a new log entry (driver's notebook record).
    """
    service = LogbookService(db)
    return service.create_entry(payload)

@router.get("/last", response_model=LogEntryRead | None)
def get_last_entry(db: Session = Depends(get_db)):
    service = LogbookService(db)
    return service.get_last_entry()

    """
    List log entries with optional date filters + pagination.
    Examples:
      /logbook/entries
      /logbook/entries?day_from=2026-02-01&day_to=2026-02-27
      /logbook/entries?limit=20&offset=0
    """
    service = LogbookService(db)
    return service.list_entries(day_from=day_from, day_to=day_to, limit=limit, offset=offset)


@router.get(
    "/entries/{entry_id}",
    response_model=LogEntryRead,
)
def get_entry(entry_id: int, db: Session = Depends(get_db)):
    """
    Get one log entry by id.
    """
    service = LogbookService(db)
    return service.get_entry(entry_id)


@router.patch(
    "/entries/{entry_id}",
    response_model=LogEntryRead,
)
def update_entry(entry_id: int, payload: LogEntryUpdate, db: Session = Depends(get_db)):
    """
    Update (partially) an existing log entry.
    """
    service = LogbookService(db)
    return service.update_entry(entry_id, payload)


@router.delete(
    "/entries/{entry_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    """
    Delete a log entry.
    """
    service = LogbookService(db)
    service.delete_entry(entry_id)
    return None