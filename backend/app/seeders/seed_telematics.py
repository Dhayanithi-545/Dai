import random

from datetime import (
    datetime,
    timedelta
)

from app.database.mongodb import (
    MongoDB
)


VEHICLE_ID = "TN-DS-545"


def clamp(
    value,
    min_value,
    max_value
):
    return max(
        min_value,
        min(
            value,
            max_value
        )
    )


def seed_telematics():

    db = MongoDB.get_database()

    # Delete old telemetry
    db.vehicle_telematics.delete_many(
        {
            "vehicle_id":
            VEHICLE_ID
        }
    )

    telematics_records = []

    current_time = datetime.now()

    # Initial realistic values
    battery_percentage = random.uniform(
        72,
        90
    )

    battery_temperature = random.uniform(
        30,
        34
    )

    motor_temperature = random.uniform(
        40,
        50
    )

    speed_kmph = random.randint(
        0,
        45
    )

    latitude = 13.0827
    longitude = 80.2707

    odometer_km = random.randint(
        1000,
        3000
    )

    for minute in range(
        59,
        -1,
        -1
    ):

        timestamp = (
            current_time
            -
            timedelta(
                minutes=minute
            )
        )

        # Vehicle moving or stopped
        is_moving = random.random() > 0.2

        if is_moving:
            speed_kmph = clamp(
                speed_kmph
                +
                random.randint(
                    -8,
                    8
                ),
                5,
                80
            )
        else:
            speed_kmph = 0

        # Charging status
        charging_status = (
            random.random() < 0.05
        )

        # Battery behavior
        if charging_status:
            battery_percentage += random.uniform(
                0.02,
                0.08
            )
        else:
            battery_percentage -= random.uniform(
                0.01,
                0.06
            )

        battery_percentage = round(
            clamp(
                battery_percentage,
                30,
                100
            ),
            2
        )

        # Battery temp changes
        battery_temperature += random.uniform(
            -0.3,
            0.4
        )

        battery_temperature = round(
            clamp(
                battery_temperature,
                28,
                45
            ),
            2
        )

        # Motor temp linked to speed
        motor_temperature += (
            speed_kmph / 100
        ) + random.uniform(
            -1,
            1
        )

        motor_temperature = round(
            clamp(
                motor_temperature,
                35,
                70
            ),
            2
        )

        # Range calculation
        range_remaining_km = round(
            battery_percentage * 1.2,
            2
        )

        # GPS movement
        if speed_kmph > 0:

            latitude += random.uniform(
                -0.0005,
                0.0005
            )

            longitude += random.uniform(
                -0.0005,
                0.0005
            )

        # Odometer increment
        odometer_km += (
            speed_kmph / 60
        )

        # Connectivity
        connectivity = (
            "offline"
            if random.random() < 0.02
            else "online"
        )

        # Fault codes
        fault_codes = []

        if motor_temperature > 65:
            fault_codes.append(
                "high_motor_temp"
            )

        if battery_percentage < 35:
            fault_codes.append(
                "battery_warning"
            )

        telematics_record = {

            "vehicle_id":
            VEHICLE_ID,

            "timestamp":
            timestamp,

            "speed_kmph":
            speed_kmph,

            "battery_percentage":
            battery_percentage,

            "battery_temperature":
            battery_temperature,

            "motor_temperature":
            motor_temperature,

            "range_remaining_km":
            range_remaining_km,

            "latitude":
            round(
                latitude,
                6
            ),

            "longitude":
            round(
                longitude,
                6
            ),

            "odometer_km":
            round(
                odometer_km,
                2
            ),

            "charging_status":
            charging_status,

            "connectivity":
            connectivity,

            "fault_codes":
            fault_codes
        }

        telematics_records.append(
            telematics_record
        )

    db.vehicle_telematics.insert_many(
        telematics_records
    )

    print(
        f"{len(telematics_records)} "
        f"telematics records seeded "
        f"for {VEHICLE_ID}"
    )