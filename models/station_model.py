from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

if TYPE_CHECKING:
    from models.readings_model import Reading

class Station(Base):
    __tablename__ = "stations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    latitude: Mapped[float] = mapped_column()
    longitude: Mapped[float] = mapped_column()

    readings: Mapped[list["Reading"]] = relationship(
        back_populates="station",
        cascade="all, delete-orphan"
    )
