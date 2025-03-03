from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent.joinpath(".env.dev").__str__())
    # Service configs
    HOST: Optional[str] = "0.0.0.0"
    PORT: Optional[int] = 8001

    # Service A credentials
    SERVICE_A_HOST: Optional[str] = "0.0.0.0"
    SERVICE_A_PORT: Optional[int] = 8002

    @property
    def SERVICE_A_URL(cls):
        return f"http://{cls.SERVICE_A_HOST}:{cls.SERVICE_A_PORT}"


settings = Settings()
