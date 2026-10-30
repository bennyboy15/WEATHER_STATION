from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import CreateStation, UpdateStation
from models.station_model import Station

router = APIRouter(prefix="/stations", tags=["stations"])

@router.get("")
def get_stations(db: Session = Depends(get_db)):
    stations = db.query(Station).all()
    return stations

@router.post("", status_code=201)
def create_station(station: CreateStation, db: Session = Depends(get_db)):
    new_station = Station(name=station.name, latitude=station.latitude, longitude=station.longitude)

    db.add(new_station)
    db.commit()
    db.refresh(new_station)

    return new_station

@router.patch("/{station_id}")
def update_station(station_id: int, station: UpdateStation, db: Session = Depends(get_db)):
    existing_station = db.get(Station, station_id)

    if existing_station is None:
        raise HTTPException(404, "Station not found")

    updates = station.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(existing_station, field, value)

    db.commit()
    db.refresh(existing_station)

    return existing_station

@router.delete("/{station_id}")
def delete_station(station_id: int, db: Session = Depends(get_db)):
    existing_station = db.get(Station, station_id)

    if existing_station is None:
        raise HTTPException(404, "Station not found")

    db.delete(existing_station)
    db.commit()

    return {"message": "Station deleted"}