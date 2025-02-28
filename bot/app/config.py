from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR: Path = Path(__file__).parents[2]
ENV_FILE_PATH: Path = BASE_DIR.joinpath(".env")
print(ENV_FILE_PATH)


class Settings(BaseSettings):
    """
    Settings class
    :var
    DB_DATABASE_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    TOKEN: str
    LOGIN: str
    PASSWORD: str
    """

    model_config = SettingsConfigDict(extra="ignore", env_file=ENV_FILE_PATH)
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    TOKEN: str
    LOGIN: str
    PASSWORD: str
    MFUA: str
    VERSION: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
