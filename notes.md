# FASTAPI RUN

fastapi dev main.py

# TESTS

python -m pytest

# CONFIG (.env or environment variables)

DATABASE_URL  default sqlite:///./weatherstation.db
API_KEY       if set, POST/PATCH/DELETE need an X-API-Key header

# ROUTES

GET    /stations
POST   /stations
PATCH  /stations/{id}
DELETE /stations/{id}                    (also deletes its readings)
GET    /stations/{id}/readings           ?start=&end=&limit= (newest first, limit 1-1000, default 100)
GET    /stations/{id}/readings/latest
POST   /stations/{id}/readings
GET    /readings/{reading_id}

# MODELS

stations
├── id
├── name
├── latitude      decimal degrees
└── longitude     decimal degrees

readings
├── id
├── station_id
├── recorded_at   stored as naive UTC, returned with Z
├── temperature   °C
├── humidity      %
├── pressure      hPa
├── rainfall      mm since previous reading
└── wind_speed    m/s
