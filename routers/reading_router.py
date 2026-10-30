from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from auth import require_api_key
from database import get_db
from schemas import CreateReading, ReadingResponse, to_utc_naive
from models.readings_model import Reading
from models.station_model import Station
from datetime import datetime

router = APIRouter(tags=["readings"])

def get_station_or_404(station_id: int, db: Session) -> Station:
    station = db.get(Station, station_id)

    if station is None:
        raise HTTPException(404, "Station not found")

    return station

@router.get("/stations/{station_id}/readings", response_model=list[ReadingResponse])
def get_station_readings(
    station_id: int,
    start: datetime | None = None,
    end: datetime | None = None,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    get_station_or_404(station_id, db)

    query = select(Reading).where(Reading.station_id == station_id)

    if start is not None:
        query = query.where(Reading.recorded_at >= to_utc_naive(start))
    if end is not None:
        query = query.where(Reading.recorded_at <= to_utc_naive(end))

    return db.scalars(
        query.order_by(Reading.recorded_at.desc()).limit(limit)
    ).all()

@router.get("/stations/{station_id}/readings/latest", response_model=ReadingResponse)
def get_station_reading_latest(station_id: int, db: Session = Depends(get_db)):
    get_station_or_404(station_id, db)

    reading = db.scalars(
        select(Reading)
        .where(Reading.station_id == station_id)
        .order_by(Reading.recorded_at.desc())
        .limit(1)
    ).first()

    if reading is None:
        raise HTTPException(404, "No readings for this station")

    return reading

@router.post("/stations/{station_id}/readings", response_model=ReadingResponse, status_code=201, dependencies=[Depends(require_api_key)])
def create_reading(station_id: int, reading: CreateReading, db: Session = Depends(get_db)):
    get_station_or_404(station_id, db)

    # Omitting recorded_at lets the column's server default (current UTC time) fill it
    new_reading = Reading(station_id=station_id, **reading.model_dump(exclude_none=True))

    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)

    return new_reading

@router.get("/readings/{reading_id}", response_model=ReadingResponse)
def get_reading(reading_id: int, db: Session = Depends(get_db)):
    reading = db.get(Reading, reading_id)

    if reading is None:
        raise HTTPException(404, "Reading not found")

    return reading
