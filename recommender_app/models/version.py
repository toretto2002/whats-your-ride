from recommender_app.extensions import db

class Version(db.Model):
    __tablename__ = 'versions'

    id = db.Column(db.Integer, primary_key=True)

    # relazione con il modello (es. RS 457)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'), nullable=False)

    # dati generali
    name = db.Column(db.String(500), nullable=False)
    year_start = db.Column(db.Integer)
    year_end = db.Column(db.Integer)
    price = db.Column(db.Float)
    warranty = db.Column(db.String(100))
    optional = db.Column(db.String(500))
    category = db.Column(db.String(100))

    # misure
    seat_height_min = db.Column(db.Float)
    seat_height_max = db.Column(db.Float)
    dry_weight = db.Column(db.Float)
    wet_weight = db.Column(db.Float)

    # motore
    displacement = db.Column(db.Float)
    engine_type = db.Column(db.String(100))
    stroke = db.Column(db.Integer)
    cylinders = db.Column(db.Integer)
    cylinder_config = db.Column(db.String(100))
    cooling = db.Column(db.String(100))
    starter = db.Column(db.String(100))
    fuel_system = db.Column(db.String(100))
    bore = db.Column(db.Float)
    stroke_length = db.Column(db.Float)
    clutch = db.Column(db.String(100))
    valves = db.Column(db.Integer)
    distribution = db.Column(db.String(100))
    ride_by_wire = db.Column(db.Boolean)
    traction_control = db.Column(db.Boolean)
    engine_maps = db.Column(db.String(100))
    power_hp = db.Column(db.Float)
    power_rpm = db.Column(db.Integer)
    torque_nm = db.Column(db.Float)
    torque_rpm = db.Column(db.Integer)
    emissions = db.Column(db.String(100))
    gearbox_type = db.Column(db.String(100))
    gears = db.Column(db.Integer)
    fuel_capacity = db.Column(db.Float)
    final_drive = db.Column(db.String(100))

    # ciclistica
    frame_type = db.Column(db.String(200))
    front_suspension = db.Column(db.String(300))
    front_travel = db.Column(db.Float)
    rear_suspension = db.Column(db.String(300))
    rear_travel = db.Column(db.Float)
    front_brake_type = db.Column(db.String(100))
    front_brake_size = db.Column(db.Float)
    rear_brake_type = db.Column(db.String(100))
    rear_brake_size = db.Column(db.Float)
    abs = db.Column(db.Boolean)
    wheel_type = db.Column(db.String(100))
    front_wheel_size = db.Column(db.String(100))
    front_tire = db.Column(db.String(200))
    rear_wheel_size = db.Column(db.String(100))
    rear_tire = db.Column(db.String(200))

    # batteria
    battery = db.Column(db.String(200))
    battery_capacity = db.Column(db.String(100))
    battery_life = db.Column(db.String(100))
    secondary_battery = db.Column(db.String(100))

    # relazione SQLAlchemy (opzionale, se vuoi fare join diretti)
    model = db.relationship("Model", backref="versions", lazy=True)
