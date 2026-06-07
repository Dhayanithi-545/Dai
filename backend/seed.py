from app.database.mongodb import (
    MongoDB
)

from app.utils.seed_vehicles import (
    seed_vehicles
)

MongoDB.connect()

seed_vehicles()