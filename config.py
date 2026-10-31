from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # extra="ignore" lets .env hold other values too (e.g. LIVE_URL for curl testing)
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./weatherstation.db"
    # When unset, write endpoints are open (handy for local dev)
    api_key: str | None = None

settings = Settings()
