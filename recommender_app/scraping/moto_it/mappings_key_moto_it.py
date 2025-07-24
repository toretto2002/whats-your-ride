# recommender_app/scraping/mappings_key.py
KEY_MAPPING = {
    # Generali
    "allestimento": "name",
    "prezzo": "price",
    "inizio_produzione": "year_start",
    "fine produzione": "year_end",
    "garanzia": "warranty",
    "optional": "optional",

    # Misure
    "lunghezza": "length", #######
    "larghezza": "width", #######
    "altezza": "height", #######
    "altezza_minima_da_terra": "min_height_from_ground", #######
    "altezza_sella_da_terra_min": "seat_height_min",
    "altezza_sella_da_terra_max": "seat_height_max",
    "interasse": "wheelbase", #######
    "peso_a_secco": "dry_weight",
    "peso_in_ordine_di_marcia": "wet_weight",

    # Motore
    "cilindrata": "displacement",
    "tipo_motore": "engine_type",
    "tempi": "stroke",
    "cilindri": "cylinders",
    "configurazione_cilindri": "cylinder_config",
    "disposizione_cilindri": "cylinder_disposition",  #######
    "inclinazione_cilindri": "cylinder_inclination",  #######
    "inclinazione_cilindri_a_v": "cylinder_inclination_v",  #######
    "raffreddamento": "cooling",
    "avviamento": "starter",
    "alimentazione": "fuel_system",
    "alesaggio": "bore",
    "corsa": "stroke_length",
    "frizione": "clutch",
    "numero_valvole": "valves",
    "distribuzione": "distribution",
    "ride_by_wire": "ride_by_wire",
    "controllo_trazione": "traction_control",
    "mappe_motore": "engine_maps",
    "potenza": "raw_power",  # verrà parsata dopo
    "coppia": "raw_torque",  # idem
    "emissioni": "emissions",
    "depotenziata": "depowered", ########
    "tipologia_cambio": "gearbox_type",
    "numero_marce": "gears",
    "presenza_retromarcia": "reverse_gear", ########
    "consumo_medio_vmtc": "average_consumption", ########
    "capacità_serbatoio_carburante": "fuel_capacity",
    "trasmissione_finale": "final_drive",

    # Ciclistica
    "telaio": "frame_type",
    "sospensione_anteriore": "front_suspension",
    "escursione_anteriore": "front_travel",
    "sospensione_posteriore": "rear_suspension",
    "escursione_posteriore": "rear_travel",
    "tipo_freno_anteriore": "front_brake_type",
    "misura_freno_anteriore": "front_brake_size",
    "tipo_freno_posteriore": "rear_brake_type",
    "misura_freno_posteriore": "rear_brake_size",
    "abs": "abs",
    "tipo_ruote": "wheel_type",
    "misura_cerchio_anteriore": "front_wheel_size",
    "pneumatico_anteriore": "front_tire",
    "misura_cerchio_posteriore": "rear_wheel_size",
    "pneumatico_posteriore": "rear_tire",

    # Batteria
    "batteria": "battery",
    "capacità": "battery_capacity",
    "autonomia_e_durata": "battery_life",
    "batteria_secondaria": "secondary_battery",
    
    #relations
    "model_id": "model_id",
}
