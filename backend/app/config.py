import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    AI_API_KEY = os.getenv("AI_API_KEY")
    AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")


settings = Settings()
