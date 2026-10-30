from pydantic import BaseModel

class CreateStation(BaseModel):
    name: str
    latitude: float
    longitude: float

class UpdateStation(BaseModel):
    name: str | None = None
    latitude: float | None = None
    longitude: float | None = None