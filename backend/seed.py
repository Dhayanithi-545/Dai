from app.database.mongodb import (
    MongoDB
)

from app.seeders.seed_vehicle_catalog import (
    seed_vehicle_catalog
)

from app.seeders.seed_plants import (
    seed_plants
)

from app.seeders.seed_vehicles import (
    seed_vehicles
)

from app.seeders.seed_manufacturing import (
    seed_manufacturing
)

from app.seeders.seed_sales import (
    seed_sales
)

from app.seeders.seed_telematics import (
    seed_telematics
)

def main():

    MongoDB.connect()

    seed_vehicle_catalog()

    seed_plants()

    seed_vehicles()

    seed_manufacturing()

    seed_sales()

    seed_telematics()

    print(
        "\nAll database "
        "collections seeded "
        "successfully"
    )


if __name__ == "__main__":

    main()