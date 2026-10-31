from sqlalchemy import create_engine, event
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings

url = make_url(settings.database_url)

if url.get_backend_name() == "sqlite":
    engine = create_engine(
        url,
        connect_args={"check_same_thread": False}
    )

    # SQLite ignores foreign keys (and ON DELETE CASCADE) unless enabled per connection
    @event.listens_for(engine, "connect")
    def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
        dbapi_connection.execute("PRAGMA foreign_keys=ON")
else:
    engine = create_engine(
        url,
        # Neon closes idle connections when it scales to zero; check each one before use
        pool_pre_ping=True
    )

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
