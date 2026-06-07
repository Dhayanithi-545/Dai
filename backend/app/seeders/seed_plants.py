from app.database.mongodb import (
    MongoDB
)


def seed_plants():

    db = MongoDB.get_database()

    db.plants.delete_many({})

    plants = [

        {
            "plant_name":
            "Chennai Plant",

            "location":
            "Tamil Nadu",

            "employees":
            420,

            "daily_capacity":
            350,

            "status":
            "Operational"
        },

        {
            "plant_name":
            "Hyderabad Plant",

            "location":
            "Telangana",

            "employees":
            380,

            "daily_capacity":
            300,

            "status":
            "Operational"
        }
    ]

    db.plants.insert_many(
        plants
    )

    print(
        "Plants seeded"
    )