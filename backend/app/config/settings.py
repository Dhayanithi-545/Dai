import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = "Dai AI Agent"
    APP_VERSION = "1.0.0"

    MONGO_URI = os.getenv("MONGO_URI")
    DATABASE_NAME = os.getenv("DATABASE_NAME")

    GOOGLE_APPLICATION_CREDENTIALS = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS"
    )

    GOOGLE_PROJECT_ID = os.getenv(
        "GOOGLE_PROJECT_ID"
    )

    GOOGLE_LOCATION = os.getenv(
        "GOOGLE_LOCATION"
    )


settings = Settings()