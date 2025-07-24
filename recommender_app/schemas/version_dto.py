from pydantic import BaseModel
from recommender_app.schemas.model_dto import ModelOut

class VersionBase(BaseModel):
    
    name: str
    year_start: int | None = None
    year_end: int | None = None
    price: float | None = None
    warranty: str | None = None
    optional: str | None = None
    seat_height_min: float | None = None
    seat_height_max: float | None = None
    dry_weight: float | None = None
    wet_weight: float | None = None
    displacement: float | None = None
    engine_type: str | None = None
    stroke: int | None = None
    cylinders: int | None = None
    cylinder_config: str | None = None
    cooling: str | None = None
    starter: str | None = None
    fuel_system: str | None = None
    bore: float | None = None
    stroke_length: float | None = None
    clutch: str | None = None
    valves: int | None = None
    distribution: str | None = None
    ride_by_wire: bool | None = None
    traction_control: bool | None = None
    engine_maps: str | None = None
    power_hp: float | None = None
    power_rpm: int | None = None
    torque_nm: float | None = None
    torque_rpm: int | None = None
    emissions: str | None = None
    gearbox_type: str | None = None
    gears: int | None = None
    fuel_capacity: float | None = None
    final_drive: str | None = None
    frame_type: str | None = None
    front_suspension: str | None = None
    front_travel: float | None = None
    rear_suspension: str | None = None
    rear_travel: float | None = None
    front_brake_type: str | None = None
    front_brake_size: float | None = None
    rear_brake_type: str | None = None
    rear_brake_size: float | None = None
    abs: bool | None = None
    wheel_type: str | None = None
    front_wheel_size: str | None = None
    front_tire: str | None = None
    rear_wheel_size: str | None = None
    rear_tire: str | None = None
    battery: str | None = None
    battery_capacity: str | None = None
    battery_life: str | None = None
    secondary_battery: str | None = None
    
    
class VersionCreate(VersionBase):
    pass

class VersionOut(VersionBase):
    id: int

    class Config:
        orm_mode = True
        
class VersionWithModel(VersionOut):
    model: ModelOut

    class Config:
        orm_mode = True
        from_attributes = True
    
    