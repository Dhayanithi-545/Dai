from pymongo import MongoClient
import certifi

from app.config.settings import (
    settings
)


class MongoDB:

    client = None
    database = None

    @classmethod
    def connect(cls):

        try:

            cls.client = MongoClient(
                settings.MONGO_URI,
                tls=True,
                tlsCAFile=certifi.where()
            )

            cls.database = cls.client[
                settings.DATABASE_NAME
            ]

            cls.client.admin.command(
                "ping"
            )

            print(
                "MongoDB Connected Successfully"
            )

        except Exception as e:

            print(
                f"MongoDB Connection Error: {e}"
            )

    @classmethod
    def get_database(cls):
        return cls.database