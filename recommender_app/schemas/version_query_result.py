from pydantic import BaseModel, Field


class VersionQueryResult(BaseModel):
    brand: str | None = None
    model: str | None = None
    version: str | None = None
    category: str | None = None
    power_hp: float | None = None
    torque_nm: float | None = None
    displacement: float | None = None
    dry_weight: float | None = None
    wet_weight: float | None = None
    seat_height_min: float | None = None
    seat_height_max: float | None = None
    price: float | None = None
    top_speed: float | None = None
    fuel_capacity: float | None = None
    raw: dict = Field(default_factory=dict)
