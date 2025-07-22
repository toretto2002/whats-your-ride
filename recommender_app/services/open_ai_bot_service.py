import logging
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core import SQLDatabase
from recommender_app.db_ses.session import llama_engine
from llama_index.embeddings.openai import OpenAIEmbedding
from recommender_app.core.config import Config  # dove hai messo la OPENAI_API_KEY

class OpenAiBotService:
    def __init__(self):
        # Logging
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
        self.logger = logging.getLogger(__name__)

        # ChatGPT LLM (via llama-index)
        self.llm = LlamaOpenAI(
            api_key=Config.OPENAI_API_KEY,
            model="gpt-4o",  # oppure "gpt-3.5-turbo"
            temperature=0.7
        )

        # Embedding model OpenAI
        Settings.embed_model = OpenAIEmbedding(api_key=Config.OPENAI_API_KEY)

        # SQL DB setup
        self.sql_database = SQLDatabase(
            llama_engine,
            include_tables=["motorcycles"],  # o rimuovi per tutte
            sample_rows_in_table_info=2,
            custom_table_info =  {
                    "motorcycles": """
                Tabella che contiene i dati tecnici e descrittivi dei modelli di motociclette.

                🔹 Informazioni generali:
                - 'id': Identificativo univoco del modello.
                - 'full_name': Nome completo del modello, solitamente composto da marca e nome.
                - 'name': Nome del modello della moto.
                - 'brand': Marca della moto.
                - 'year_of_manufacture': Anno di produzione della moto.
                - 'usage_style': Categoria della moto (es. naked, sport, touring, enduro, cruiser).

                🔹 Specifiche motore:
                - 'displacement': Cilindrata del motore in centimetri cubici (cc).
                - 'type_of_engine': Tipo di architettura motore (es. V2, inline 4, monocilindrico).
                - 'engine_details': Descrizione dettagliata del motore.
                - 'power': Potenza massima in cavalli (hp).
                - 'max_rpm': Numero massimo di giri del motore al minuto.
                - 'torque': Coppia massima in Nm.
                - 'compression_ratio': Rapporto di compressione.
                - 'bore_x_stroke': Alesaggio e corsa.
                - 'valves_per_cylinder': Numero di valvole per cilindro.
                - 'fuel_system': Tipo di alimentazione (es. iniezione, carburatore).
                - 'fuel_control': Controllo del carburante.
                - 'ignition': Tipo di accensione.
                - 'lubrification_system': Sistema di lubrificazione.
                - 'cooling_system': Sistema di raffreddamento (es. aria, liquido).

                🔹 Trasmissione:
                - 'transmission': Tipo di cambio (es. manuale, automatico).
                - 'transmission_type': Specifica del tipo (es. a catena, cardano).
                - 'clutch': Tipo di frizione.
                - 'drive_line': Linea di trasmissione.
                - 'final_drive': Tipo di trasmissione finale (catena, cardano, cinghia).

                🔹 Consumi ed emissioni:
                - 'fuel_consumption': Consumo di carburante in L/100km.
                - 'fuel_tank_capacity': Capacità del serbatoio in litri.
                - 'greenhouse_gas_emissions': Emissioni di CO₂ in g/km.
                - 'emission_class': Classe di omologazione (es. Euro 5).
                - 'power_to_weight_ratio': Rapporto potenza/peso.

                🔹 Ciclistica:
                - 'frame_type': Tipo di telaio.
                - 'fork_angle': Angolo del cannotto di sterzo.
                - 'trail': Avancorsa.
                - 'front_suspension': Sospensione anteriore.
                - 'front_wheel_travel': Escursione ruota anteriore (mm).
                - 'rear_suspension': Sospensione posteriore.
                - 'rear_wheel_travel': Escursione ruota posteriore (mm).
                - 'front_tire': Misura pneumatico anteriore.
                - 'rear_tire': Misura pneumatico posteriore.
                - 'front_brake': Tipo di freno anteriore.
                - 'front_brake_diameter': Diametro disco anteriore (mm).
                - 'rear_brake': Tipo di freno posteriore.
                - 'rear_brake_diameter': Diametro disco posteriore (mm).
                - 'wheels': Informazioni sulle ruote.

                🔹 Peso e dimensioni:
                - 'dry_weight': Peso a secco in kg.
                - 'wet_weight': Peso in ordine di marcia (kg).
                - 'seat_height': Altezza sella (mm).
                - 'alternative_seat_height': Altezza sella alternativa (se presente).
                - 'seat_number': Numero di posti a sedere.
                - 'overall_length', 'overall_width', 'overall_height': Dimensioni complessive (mm).
                - 'ground_clearance': Altezza da terra (mm).
                - 'wheelbase': Interasse (mm).
                - 'fuel_capacity': Capacità carburante in litri.
                - 'reserve_capacity': Capacità della riserva in litri.
                - 'carrying_capacity': Capacità di carico.
                - 'oil_capacity': Capacità olio motore (litri).

                🔹 Altro:
                - 'color_options': Colori disponibili.
                - 'starter_type', 'starter': Tipo di avviamento.
                - 'light': Tipo di fanali.
                - 'bike_peculiarities': Caratteristiche peculiari del modello.
                - 'price': Prezzo indicativo in euro.
                - 'source_url': URL della fonte dati.
                - 'top_speed': Velocità massima in km/h.
                - 'factory_warranty': Garanzia ufficiale.
                - 'battery': Tipo di batteria.
                - 'strumentation': Tipo di strumentazione presente.

                NOTE:
                - Le unità di misura sono coerenti: peso in kg, distanza in mm, potenza in CV, cilindrata in cc.
                - Alcuni valori possono essere nulli: il modello deve considerarli assenti e non filtrabili.
                """
                }

        )

        # Query engine
        self.query_engine = NLSQLTableQueryEngine(
            sql_database=self.sql_database,
            llm=self.llm,
            system_prompt = """
                Sei un esperto di motociclette e assistente virtuale per la scelta del modello ideale.

                Lavori interrogando una tabella SQL chiamata `motorcycles` che contiene dati dettagliati sui modelli disponibili. La tua funzione è rispondere alle richieste degli utenti traducendole in query SQL corrette, basandoti esclusivamente sulle informazioni contenute in questa tabella.

                🎯 Obiettivo:
                - Trova motociclette che soddisfano i criteri specificati dall'utente.
                - Se non ci sono risultati esatti, suggerisci alternative simili o con tolleranza su uno o più valori (es. 5% di margine su peso o potenza).
                - Se una colonna è nullable e non ci sono dati, comunica l’assenza di informazioni con gentilezza.
                - Se l’utente applica un filtro (es. peso < 200 kg) o un ordinamento (es. più potente), escludi automaticamente i record in cui il valore della colonna è NULL. Non devono comparire nei risultati.

                📊 Campi principali della tabella:
                - `brand`, `name`, `full_name`: identificano il modello.
                - `usage_style`: stile della moto. Valori comuni: naked, sport, enduro, touring, cruiser, offroad, custom.
                - `year_of_manufacture`: anno di produzione.
                - `dry_weight`, `wet_weight`: peso in kg.
                - `power`: potenza massima in cavalli (CV).
                - `displacement`: cilindrata in cc.
                - `type_of_engine`, `engine_details`: tipo e descrizione del motore.
                - `seat_height`: altezza sella in mm.
                - `fuel_consumption`: consumo carburante in L/100km.
                - `fuel_tank_capacity`: capacità serbatoio in litri.
                - `price`: prezzo indicativo in euro.
                - `top_speed`: velocità massima in km/h.

                📌 Unità di misura:
                - peso: kg
                - cilindrata: cc
                - potenza: cavalli (CV)
                - consumo: litri/100 km
                - altezza sella, dimensioni: millimetri (mm)
                - velocità: km/h
                - anno: intero (es. 2020)

                ✅ Considerazioni:
                - Le query devono filtrare **solo sui dati presenti nel database**.
                - Se l’utente chiede una "moto leggera", considera `dry_weight < 180` kg.
                - Se dice “cilindrata sopra i 600”, considera `displacement > 600`.
                - Se chiede una “sportiva veloce”, considera `usage_style ILIKE '%sport%' AND top_speed > 200`.
                - Se chiede una moto per "principianti", considera `power < 50` e `seat_height < 800`.

                ✋ Attenzione:
                - Non inventare dati: usa solo i campi reali.
                - Non dare mai suggerimenti fuori dal dataset.
                - Se non trovi risultati esatti, prova a suggerire alternative vicine motivando le differenze.

                🧠 Esempi di domande valide:
                - "Cerco una naked del 2020 con peso sotto i 180 kg"
                - "Vorrei una enduro con almeno 300 km di autonomia"
                - "Una sportiva con più di 100 cavalli e meno di 200 kg"
                - "Moto turistica con serbatoio capiente e comoda per due"

                Fornisci sempre una risposta chiara e focalizzata. Se i dati non sono sufficienti, invita l'utente a riformulare la richiesta o a rilassare i filtri.
                """
        )

    def ask(self, data):
        try:
            query = self.query_engine.retriever.retrieve(data)[0].raw_query
            logging.debug(f"Generated SQL Query: {query}")
        except Exception as e:
            logging.error(f"SQL Error: {e}")

        try:
            response = self.query_engine.query(data)
            return str(response)
        except Exception as e:
            logging.error(f"Execution Error: {e}")
            return {"error": str(e)}
