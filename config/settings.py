from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # API connection
    API_URL: str = "http://localhost:8000/api/v1"

    # App metadata
    APP_NAME: str = "My Streamlit App"
    APP_ICON: str = "🚀"



# Singleton — import this everywhere
settings = Settings()
