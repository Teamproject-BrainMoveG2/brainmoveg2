from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    dbuser: str
    host: str
    port: int
    password: str
    database:str

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

settings = Settings()
