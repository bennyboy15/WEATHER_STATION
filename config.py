from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = "sqlite:///./weatherstation.db"
    # When unset, write endpoints are open (handy for local dev)
    api_key: str | None = None

settings = Settings()
