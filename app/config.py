from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODEL_NAME: str 
    BASE_URL: str

    model_config = SettingsConfigDict(env_file="app/.env")
    
    
    
class DBSettings(BaseSettings):    
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT:str


    model_config = SettingsConfigDict(env_file="app/db.env")