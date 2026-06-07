from app.database.mongodb import (
    MongoDB
)


def seed_vehicle_catalog():

    db = MongoDB.get_database()

    db.vehicle_catalog.delete_many({})

    vehicles = [

        {
            "model_name":
            "Dhaya Volt",

            "category":
            "E-Bicycle",

            "range_km":
            120,

            "top_speed":
            45,

            "price":
            85000,

            "description":
            (
                "Urban commuter "
                "e-bicycle with "
                "adaptive torque sensing"
            )
        },

        {
            "model_name":
            "Glide Pro X",

            "category":
            "Hoverboard",

            "range_km":
            35,

            "top_speed":
            28,

            "price":
            55000,

            "description":
            (
                "Self-balancing "
                "hoverboard for "
                "next generation mobility"
            )
        },

        {
            "model_name":
            "EV-9 Titan",

            "category":
            "E-Truck",

            "range_km":
            480,

            "top_speed":
            120,

            "price":
            1450000,

            "description":
            (
                "Heavy-duty electric "
                "cargo truck "
                "with zero emissions"
            )
        }
    ]

    db.vehicle_catalog.insert_many(
        vehicles
    )

    print(
        "Vehicle catalog seeded"
    )