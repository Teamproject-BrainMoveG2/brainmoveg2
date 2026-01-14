from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    user: str
    host: str
    port: int
    password: str
    database:str

    model_config = SettingsConfigDict(env_file=".env")