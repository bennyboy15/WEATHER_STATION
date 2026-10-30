from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

if TYPE_CHECKING:
    from models.station_model import Station

class Reading(Base):
    __tablename__ = "readings"
    __table_args__ = (
        Index("ix_readings_station_time", "station_id", "recorded_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    station_id: Mapped[int] = mapped_column(
        ForeignKey("stations.id", ondelete="CASCADE")
    )

    station: Mapped["Station"] = relationship(
        back_populates="readings"
    )

    # Stored as naive UTC (SQLite can't store offsets); schemas.py handles conversion
    recorded_at: Mapped[datetime] = mapped_column(server_default=func.now())
    temperature: Mapped[float] = mapped_column()
    humidity: Mapped[float] = mapped_column()
    pressure: Mapped[float] = mapped_column()
    rainfall: Mapped[float] = mapped_column()
    wind_speed: Mapped[float] = mapped_column()
