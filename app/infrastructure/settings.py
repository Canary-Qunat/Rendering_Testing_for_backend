from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    #jwt
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 10
    refresh_token_days: int = 30

    #postgres
    postgres_user: str = "user"
    postgres_password: str = "password"
    postgres_db: str = "canary"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings() #type: ignore