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


def generate_vehicle_id():

    state_code = random.choice(
        [
            "TN",
            "TS"
        ]
    )

    return (
        f"{state_code}"
        f"-EV-"
        f"{random.randint(100,999)}"
    )


def get_status(
    battery_health,
    temperature
):

    if (
        battery_health < 60
        or temperature > 45
    ):

        return "Critical"

    if (
        battery_health < 80
        or temperature > 38
    ):

        return (
            "Needs Attention"
        )

    return "Healthy"


def seed_vehicles():

    db = MongoDB.get_database()

    db.vehicles.delete_many(
        {}
    )

    vehicles = []

    for _ in range(120):

        model = (
            random.choice(
                MODELS
            )
        )

        battery_health = (
            random.randint(
                50,
                100
            )
        )

        temperature = (
            random.randint(
                25,
                50
            )
        )

        range_km = {

            "Dhaya Volt":
            random.randint(
                90,
                120
            ),

            "Glide Pro X":
            random.randint(
                20,
                35
            ),

            "EV-9 Titan":
            random.randint(
                350,
                480
            )

        }[model]

        maintenance_due = (
            random.choice(
                [
                    True,
                    False
                ]
            )
        )

        vehicle = {

            "vehicle_id":
            generate_vehicle_id(),

            "model_name":
            model,

            "plant":
            random.choice(
                PLANTS
            ),

            "manufactured_date":
            (
                datetime.now()
                -
                timedelta(
                    days=
                    random.randint(
                        1,
                        180
                    )
                )
            ),

            "battery_health":
            battery_health,

            "temperature":
            temperature,

            "range_km":
            range_km,

            "status":
            get_status(
                battery_health,
                temperature
            ),

            "maintenance_due":
            maintenance_due,

            "last_service_date":
            (
                datetime.now()
                -
                timedelta(
                    days=
                    random.randint(
                        5,
                        90
                    )
                )
            ),

            "maintenance_notes":
            random.choice([
                "Battery overheating",
                "Brake inspection required",
                "Routine maintenance",
                "Motor calibration needed",
                "No issues"
            ])
        }

        vehicles.append(
            vehicle
        )

    db.vehicles.insert_many(
        vehicles
    )

    print(
        "120 vehicles seeded"
    )