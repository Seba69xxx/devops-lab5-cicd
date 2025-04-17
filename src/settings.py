import os

class Settings:
    SERVER_ADDR: str = os.getenv("SERVER_ADDR", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))

settings = Settings()

print(f"Settings loaded: SERVER_ADDR={settings.SERVER_ADDR}, SERVER_PORT={settings.SERVER_PORT}")
