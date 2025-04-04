from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(...)

    class Config:
        env_file = ".env"


settings = Settings()
print(settings.database_url)
