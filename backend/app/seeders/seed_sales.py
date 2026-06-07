import random

from datetime import (
    datetime,
    timedelta
)

from app.database.mongodb import (
    MongoDB
)


MODELS = {

    "Dhaya Volt":
    85000,

    "Glide Pro X":
    55000,

    "EV-9 Titan":
    1450000
}

CITIES = [

    "Chennai",
    "Hyderabad",
    "Bangalore",
    "Mumbai",
    "Delhi",
    "Pune"
]


def seed_sales():

    db = MongoDB.get_database()

    db.sales_data.delete_many(
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

        for city in CITIES:

            for model, price in (
                MODELS.items()
            ):

                units = (
                    random.randint(
                        2,
                        25
                    )
                )

                record = {

                    "date":
                    date,

                    "city":
                    city,

                    "model":
                    model,

                    "units_sold":
                    units,

                    "revenue":
                    (
                        units
                        *
                        price
                    )
                }

                records.append(
                    record
                )

    db.sales_data.insert_many(
        records
    )

    print(
        "Sales data seeded"
    )