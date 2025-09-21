import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"

print(f"🔍 Loading .env from: {env_path}")
load_dotenv(dotenv_path=env_path)

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

settings = Settings()

print("✅ OPENAI_API_KEY loaded:", bool(settings.OPENAI_API_KEY))