from pydantic import BaseSettings

class Settings(BaseSettings):
    BATCH_SIZE: int = 10
    OUTPUT_DIR: str = "./output"
    LOG_LEVEL: str = "INFO"
    PAGE_TIMEOUT: int = 60000
    WAIT_UNTIL: str = "networkidle"
    
    class Config:
        env_file = ".env"

settings = Settings()