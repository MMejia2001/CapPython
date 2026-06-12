from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Final Orders Service"
    app_env: str = "dev"
    debug: bool = True
    database_url: str = "sqlite:///./orders.db"
    api_key: SecretStr = SecretStr("demo-key")

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")


settings = Settings()
