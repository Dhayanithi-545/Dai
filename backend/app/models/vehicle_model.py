from pydantic import BaseModel


class Vehicle(BaseModel):

    vehicle_id: str

    battery_health: int

    temperature: int

    status: str

    range_km: int

    maintenance_due: bool