from pydantic import BaseModel
from datetime import datetime

# -- STATIONS --
class CreateStation(BaseModel):
    name: str
    latitude: float
    longitude: float

class UpdateStation(BaseModel):
    name: str | None = None
    latitude: float | None = None
    longitude: float | None = None

# -- READINGS --
class CreateReading(BaseModel):
    station_id: int
    recorded_at: datetime
    temperature: float
    humidity: float
    pressure: float
    rainfall: float
    wind_speed: float