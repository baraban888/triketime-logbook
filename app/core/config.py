from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "TrikeTime Logbook"
    database_url: str = "sqlite:///./triketime.db"


settings = Settings()