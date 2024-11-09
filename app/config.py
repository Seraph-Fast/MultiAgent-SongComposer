from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODEL_NAME: str 
    BASE_URL: str

    model_config = SettingsConfigDict(env_file="app/.env")