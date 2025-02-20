import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Astro"
    API_VERSION: str = "1.0"
    PORT: int = 8100  # Port de l'API

settings = Settings()
