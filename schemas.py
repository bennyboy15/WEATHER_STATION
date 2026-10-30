from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime, timezone

def to_utc_naive(value: datetime) -> datetime:
    """Convert to naive UTC for storage. Naive input is assumed to already be UTC."""
    if value.tzinfo is not None:
        value = value.astimezone(timezone.utc).replace(tzinfo=None)
    return value

# -- STATIONS --
StationName = Annotated[str, Field(min_length=1, max_length=255)]
Latitude = Annotated[float, Field(ge=-90, le=90, description="Decimal degrees")]
Longitude = Annotated[float, Field(ge=-180, le=180, description="Decimal degrees")]

class StationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    latitude: float
    longitude: float

class CreateStation(BaseModel):
    name: StationName
    latitude: Latitude
    longitude: Longitude

class UpdateStation(BaseModel):
    name: StationName | None = None
    latitude: Latitude | None = None
    longitude: Longitude | None = None

    # Fields may be omitted, but not explicitly set to null (the columns are NOT NULL)
    @field_validator("*")
    @classmethod
    def reject_null(cls, value):
        if value is None:
            raise ValueError("cannot be null")
        return value

# -- READINGS --
class ReadingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    station_id: int
    recorded_at: datetime
    temperature: float
    humidity: float
    pressure: float
    rainfall: float
    wind_speed: float

    @field_validator("recorded_at")
    @classmethod
    def mark_utc(cls, value: datetime) -> datetime:
        return value.replace(tzinfo=timezone.utc)

class CreateReading(BaseModel):
    recorded_at: datetime | None = Field(None, description="Defaults to now (UTC). Naive values are treated as UTC.")
    temperature: float = Field(ge=-100, le=100, description="°C")
    humidity: float = Field(ge=0, le=100, description="Relative humidity, %")
    pressure: float = Field(ge=300, le=1100, description="hPa")
    rainfall: float = Field(ge=0, description="mm since the previous reading")
    wind_speed: float = Field(ge=0, description="m/s")

    @field_validator("recorded_at")
    @classmethod
    def normalise_recorded_at(cls, value: datetime | None) -> datetime | None:
        return None if value is None else to_utc_naive(value)
