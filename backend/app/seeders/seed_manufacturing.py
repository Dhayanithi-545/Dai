import random

from datetime import (
    datetime,
    timedelta
)

from app.database.mongodb import (
    MongoDB
)


MODELS = [

    "Dhaya Volt",
    "Glide Pro X",
    "EV-9 Titan"
]

PLANTS = [

    "Chennai Plant",
    "Hyderabad Plant"
]


def seed_manufacturing():

    db = MongoDB.get_database()

    db.manufacturing_data.delete_many(
        {}
    )

    records = []

    for day in range(90):

        date = (
            datetime.now()
            -
            timedelta(
                days=day
            )
        )

        for plant in PLANTS:

            for model in MODELS:

                record = {

                    "date":
                    date,

                    "plant":
                    plant,

                    "model":
                    model,

                    "produced_count":
                    random.randint(
                        20,
                        100
                    ),

                    "defect_count":
                    random.randint(
                        0,
                        10
                    ),

                    "efficiency":
                    random.randint(
                        80,
                        99
                    )
                }

                records.append(
                    record
                )

    db.manufacturing_data.insert_many(
        records
    )

    print(
        "Manufacturing data seeded"
    )