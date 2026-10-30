from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import CreateReading
from models.readings_model import Reading
from models.station_model import Station

router = APIRouter(prefix="/readings", tags=["readings"])

@router.get("")
def get_readings(db: Session = Depends(get_db)):
    readings = db.query(Reading).all()
    return readings

@router.get("/{station_id}")
def get_station_readings(station_id: int, db: Session = Depends(get_db)):
    station = db.get(Station, station_id)

    if station is None:
        raise HTTPException(404, "Station not found")

    return station.readings

@router.post("", status_code=201)
def create_reading(reading: CreateReading, db: Session = Depends(get_db)):
    new_reading = Reading(
        station_id=reading.station_id,
        recorded_at=reading.recorded_at,
        temperature=reading.temperature,
        humidity=reading.humidity,
        pressure=reading.pressure,
        rainfall=reading.rainfall,
        wind_speed=reading.wind_speed,
    )

    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)

    return new_reading
