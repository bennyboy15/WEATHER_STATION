from fastapi import FastAPI
from database import Base, engine
from models import station_model, readings_model  # noqa: F401
from routers.station_router import router as stations_router
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(stations_router)

