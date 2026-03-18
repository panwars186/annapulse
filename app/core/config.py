import os
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv


load_dotenv()


class Settings:
    """
    Central configuration object for the application.
    """

    database_url: str
    jwt_secret: str
    razorpay_key_id: Optional[str]
    razorpay_key_secret: Optional[str]

    def __init__(self) -> None:
        db_url = os.getenv("DATABASE_URL")
        jwt_secret = os.getenv("JWT_SECRET")

        if not db_url:
            raise RuntimeError("DATABASE_URL environment variable is not set")
        if not jwt_secret:
            raise RuntimeError("JWT_SECRET environment variable is not set")

        self.database_url = db_url
        self.jwt_secret = jwt_secret
        self.razorpay_key_id = os.getenv("RAZORPAY_KEY_ID")
        self.razorpay_key_secret = os.getenv("RAZORPAY_KEY_SECRET")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

DATABASE_URL = settings.database_url
JWT_SECRET = settings.jwt_secret
RAZORPAY_KEY_ID = settings.razorpay_key_id
RAZORPAY_KEY_SECRET = settings.razorpay_key_secret
