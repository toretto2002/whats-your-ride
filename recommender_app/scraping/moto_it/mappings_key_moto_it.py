# recommender_app/scraping/mappings_key.py
KEY_MAPPING = {
    # Generali
    "Marca": "brand_name",
    "Modello": "model_name",
    "Allestimento": "name",
    "Categoria": "category",
    "Prezzo": "price",
    "Inizio produzione": "year_start",
    "Fine produzione": "year_end",
    "Garanzia": "warranty",
    "Optional": "optional",

    # Misure
    "Altezza sella da terra MIN": "seat_height_min",
    "Altezza sella da terra MAX": "seat_height_max",
    "Peso a secco": "dry_weight",
    "Peso in ordine di marcia": "wet_weight",

    # Motore
    "Cilindrata": "displacement",
    "Tipo motore": "engine_type",
    "Tempi": "stroke",
    "Cilindri": "cylinders",
    "Configurazione cilindri": "cylinder_config",
    "Raffreddamento": "cooling",
    "Avviamento": "starter",
    "Alimentazione": "fuel_system",
    "Alesaggio": "bore",
    "Corsa": "stroke_length",
    "Frizione": "clutch",
    "Numero valvole": "valves",
    "Distribuzione": "distribution",
    "Ride by Wire": "ride_by_wire",
    "Controllo trazione": "traction_control",
    "Mappe motore": "engine_maps",
    "Potenza": "raw_power",  # verrà parsata dopo
    "Coppia": "raw_torque",  # idem
    "Emissioni": "emissions",
    "Tipologia cambio": "gearbox_type",
    "Numero marce": "gears",
    "Capacità serbatoio carburante": "fuel_capacity",
    "Trasmissione finale": "final_drive",

    # Ciclistica
    "Telaio": "frame_type",
    "Sospensione anteriore": "front_suspension",
    "Escursione anteriore": "front_travel",
    "Sospensione posteriore": "rear_suspension",
    "Escursione posteriore": "rear_travel",
    "Tipo freno anteriore": "front_brake_type",
    "Misura freno anteriore": "front_brake_size",
    "Tipo freno posteriore": "rear_brake_type",
    "Misura freno posteriore": "rear_brake_size",
    "ABS": "abs",
    "Tipo ruote": "wheel_type",
    "Misura cerchio anteriore": "front_wheel_size",
    "Pneumatico anteriore": "front_tire",
    "Misura cerchio posteriore": "rear_wheel_size",
    "Pneumatico posteriore": "rear_tire",

    # Batteria
    "Batteria": "battery",
    "Capacità": "battery_capacity",
    "Autonomia e durata": "battery_life",
    "Batteria secondaria": "secondary_battery"
}
