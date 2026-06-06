from pymongo import MongoClient
from app.config.settings import settings


class MongoDB:

    client = None
    database = None

    @classmethod
    def connect(cls):
        try:
            cls.client = MongoClient(
                settings.MONGO_URI
            )

            cls.database = cls.client[
                settings.DATABASE_NAME
            ]

            print("MongoDB Connected Successfully")

        except Exception as e:
            print(
                f"MongoDB Connection Error: {e}"
            )

    @classmethod
    def get_database(cls):
        return cls.database