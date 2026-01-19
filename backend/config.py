from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    dbuser: str
    host: str
    port: int
    password: str
    database:str

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

settings = Settings()
def print_db_settings():
    s = Settings()
    print("[DEBUG] DB settings loaded:")
    print("  username=", repr(s.dbuser))
    print("  host=", repr(s.host))
    print("  port=", repr(s.port))
    print("  password=", repr(s.password))
    print("  database=", repr(s.database))

print_db_settings()