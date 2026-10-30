from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from auth import require_api_key
from database import get_db
from schemas import CreateStation, UpdateStation, StationResponse
from models.station_model import Station

router = APIRouter(prefix="/stations", tags=["stations"])

@router.get("", response_model=list[StationResponse])
def get_stations(db: Session = Depends(get_db)):
    return db.scalars(select(Station).order_by(Station.id)).all()

@router.post("", response_model=StationResponse, status_code=201, dependencies=[Depends(require_api_key)])
def create_station(station: CreateStation, db: Session = Depends(get_db)):
    new_station = Station(**station.model_dump())

    db.add(new_station)
    db.commit()
    db.refresh(new_station)

    return new_station

@router.patch("/{station_id}", response_model=StationResponse, dependencies=[Depends(require_api_key)])
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

@router.delete("/{station_id}", status_code=204, dependencies=[Depends(require_api_key)])
def delete_station(station_id: int, db: Session = Depends(get_db)):
    existing_station = db.get(Station, station_id)

    if existing_station is None:
        raise HTTPException(404, "Station not found")

    db.delete(existing_station)
    db.commit()
