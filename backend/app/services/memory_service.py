from datetime import datetime

from app.database.mongodb import (
    MongoDB
)


class MemoryService:

    COLLECTION_NAME = (
        "conversation_memory"
    )

    DEFAULT_SESSION_ID = (
        "default_user"
    )

    @classmethod
    async def save_vehicle_context(
        cls,
        vehicle_id: str
    ):

        db = MongoDB.get_database()

        db[
            cls.COLLECTION_NAME
        ].update_one(

            {
                "session_id":
                cls.DEFAULT_SESSION_ID
            },

            {
                "$set": {

                    "last_vehicle_id":
                    vehicle_id,

                    "updated_at":
                    datetime.utcnow()
                }
            },

            upsert=True
        )

    @classmethod
    async def get_last_vehicle(
        cls
    ):

        db = MongoDB.get_database()

        memory = db[
            cls.COLLECTION_NAME
        ].find_one({
            "session_id":
            cls.DEFAULT_SESSION_ID
        })

        if not memory:
            return None

        return memory.get(
            "last_vehicle_id"
        )