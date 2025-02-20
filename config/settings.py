import os
from dotenv import load_dotenv

load_dotenv('/mnt/ASTRO/.env')

class Settings:
    PROJECT_NAME: str = "Astro"
    API_VERSION: str = "1.0"
    PORT: int = 8100

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    DB_PATH: str = "/mnt/ASTRO/astro_memory.db"

settings = Settings()
