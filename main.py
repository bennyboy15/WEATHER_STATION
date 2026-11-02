from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from models import station_model, readings_model  # noqa: F401
from routers.station_router import router as stations_router
from routers.reading_router import router as readings_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://your-frontend.app"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(stations_router)
app.include_router(readings_router)
