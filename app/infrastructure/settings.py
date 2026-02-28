from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 10
    refresh_token_days: int = 30

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  #type: ignore