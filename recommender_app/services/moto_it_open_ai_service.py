import json
import logging
import re
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.retrievers import NLSQLRetriever
from llama_index.core import SQLDatabase
from recommender_app.db_ses.session import llama_engine
from llama_index.embeddings.openai import OpenAIEmbedding
from recommender_app.core.config import Config  # dove hai messo la OPENAI_API_KEY
from recommender_app.utils.file_loader import load_prompt
from recommender_app.services.session_service import SessionService
from recommender_app.services.category_service import CategoryService
from recommender_app.services.answer_bot_service import AnswerBotService
from recommender_app.schemas.version_query_result import VersionQueryResult
from sqlalchemy import text

FIELD_ALIAS_MAP = {
    'name': 'model',
    'model': 'model',
    'model_name': 'model',
    'models.name': 'model',
    'brand': 'brand',
    'brand_name': 'brand',
    'brands.name': 'brand',
    'category': 'category',
    'category_name': 'category',
    'categories.name': 'category',
    'version': 'version',
    'version_name': 'version',
    'versions.name': 'version',
    'power': 'power_hp',
    'power_hp': 'power_hp',
    'horsepower': 'power_hp',
    'kw': 'power_hp',
    'torque': 'torque_nm',
    'torque_nm': 'torque_nm',
    'dryweight': 'dry_weight',
    'dry_weight': 'dry_weight',
    'wetweight': 'wet_weight',
    'wet_weight': 'wet_weight',
}

TOP_TABLE_ROWS = 25


class MotoItOpenAiBotService:
    def __init__(self):
        # Logging
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
        self.logger = logging.getLogger(__name__)
        self.session_service = SessionService()
        self.category_service = CategoryService()
        self.answer_bot_service = AnswerBotService()


        # ChatGPT LLM (via llama-index)
        self.llm = LlamaOpenAI(
            api_key=Config.OPENAI_API_KEY,
            model="gpt-4o",  # oppure "gpt-3.5-turbo"
            temperature=0.5
        )

        # Embedding model OpenAI
        Settings.embed_model = OpenAIEmbedding(api_key=Config.OPENAI_API_KEY)

        # SQL DB setup
        self.sql_database = SQLDatabase(
            llama_engine,                 # il tuo SQLAlchemy Engine
            schema="public",              # opzionale: metti lo schema giusto
            include_tables=["versions_enriched"],  # solo la view
            view_support=True,            # <-- questo abilita le VIEW
            sample_rows_in_table_info=0,
            custom_table_info={
                "versions_enriched": load_prompt(
                    "utils/prompts/moto_it/versions_enriched_table_info.txt"
                )
            },
        )
        

        # Query engine
        self.query_engine = NLSQLTableQueryEngine(
            sql_database=self.sql_database,
            llm=self.llm,
            system_prompt = load_prompt("utils/prompts/moto_it/system_prompt.txt")
        )
        
        self.retriever = NLSQLRetriever(
            sql_database=self.sql_database,
            llm=self.llm,
            system_prompt= load_prompt("utils/prompts/moto_it/system_prompt.txt"),
        )

    def _synthesize_answer(self, user_message: str, sql_query: str, rows: list[dict], session_id: int) -> str:
        # Use the AnswerBotService to generate a synthesized answer
        history_msgs = self.session_service.get_messages(session_id)
        history_msgs_dict = [m.model_dump() for m in history_msgs]
        history_summary = self.answer_bot_service.summarize_history(history_msgs_dict)

        results_payload = self.answer_bot_service.compress_results(rows, user_message)
        results_json = json.dumps(results_payload, indent=2, ensure_ascii=False)
        
        prompt = load_prompt("utils/prompts/moto_it/answer_llm_system_prompt.txt")
        prompt = prompt.format(
            user_question=user_message,
            sql_query=sql_query or "N/A",
            history_summary=history_summary,
            results_json=results_json,
            max_table_rows=TOP_TABLE_ROWS
        )
        
        answer_llm = LlamaOpenAI(
            api_key=Config.OPENAI_API_KEY,
            model="gpt-4o",  # oppure "gpt-3.5-turbo"
            temperature=0.5
        )
        
        try:
            completion = answer_llm.chat(
                messages=[
                    {"role": "system", "content": load_prompt("utils/prompts/moto_it/answer_bot_system_prompt.txt")},
                    {"role": "user", "content": user_message},
                ]
            )
            
            return completion.message.content.strip()
        
        except Exception as exc:
            logging.error(f"LLM prediction error: {exc}")
            return "Sorry, I encountered an error while generating the answer."

    def ask(self, message: str, session_id: int | None = None) -> dict:
        
        prompt = self._build_retriever_prompt()
        
        self.retriever = NLSQLRetriever(
            sql_database=self.sql_database,
            llm=self.llm,
            system_prompt=prompt,
        )

        
        if not session_id:
            # TODO: recuperare l'ID reale dell'utente autenticato quando disponibile
            user_id = 1
            session_id = self.session_service.create_session(user_id=user_id)

        self.session_service.append_message(session_id, message, sender="user")

        sql_query = None
        rows: list[dict] = []

        try:
            retrievals = self.retriever.retrieve(message)
            if retrievals:
                node = retrievals[0]
                metadata = getattr(node, 'metadata', {}) or {}
                sql_query = metadata.get('sql_query') or getattr(node, 'raw_query', None)
                logging.debug(f"Generated SQL Query: {sql_query}")
        except Exception as exc:
            logging.error(f"SQL retrieval error: {exc}")

        if sql_query:
            normalized_query = self._make_query_case_insensitive(sql_query)
            normalized_query = self._enforce_select_all(normalized_query)
            if normalized_query != sql_query:
                logging.debug(f"Normalized SQL Query: {normalized_query}")
            sql_query = normalized_query
            rows = self._execute_sql_query(sql_query)

        answer = ""
        if rows:
            answer = self._synthesize_answer(message, sql_query, rows, session_id)
        else:
            # fallback sensato quando 0 risultati
            answer = self._synthesize_answer(message, sql_query, [], session_id)

        self.session_service.append_message(session_id, answer, sender="bot")

        return {
            'session_id': session_id,
            'sql_query': sql_query,
            'rows': rows,
            'answer': answer
        }

    def _execute_sql_query(self, sql_query: str) -> list[dict]:
        structured_rows: list[dict] = []
        try:
            with self.sql_database.engine.connect() as connection:
                result = connection.execute(text(sql_query))
                columns = list(result.keys())
                for raw_row in result:
                    row_dict = dict(zip(columns, raw_row))
                    structured_rows.append(self._structure_row(row_dict))
        except Exception as exc:
            logging.error(f"SQL execution error: {exc}")
        return structured_rows
    
    def _build_retriever_prompt(self) -> str:
        base_prompt = load_prompt("utils/prompts/moto_it/system_prompt.txt")
        categories = CategoryService().list_categories()
        names = ", ".join(cat.name for cat in categories)
        return base_prompt.replace("[PROMPT PER CATEGORIE]", f"Le uniche categorie valide sono: {names}. Quando applichi un filtro su category_name devi usare ESATTAMENTE una di queste stringhe, uguale lettera per lettera; se l’utente usa sinonimi, scegli il valore più vicino dalla lista di categorie che ti ho fornito. Se sei in dubbio tra piu categorie includile TUTTE nel filtro.")

    @staticmethod
    def _structure_row(row_dict: dict) -> dict:
        lower_map = {k.lower(): v for k, v in row_dict.items() if isinstance(k, str)}
        alias_values = {}
        for key, value in row_dict.items():
            if not isinstance(key, str):
                continue
            alias = FIELD_ALIAS_MAP.get(key) or FIELD_ALIAS_MAP.get(key.lower())
            if alias:
                alias_values.setdefault(alias, value)
        data = {'raw': row_dict}
        for field_name in VersionQueryResult.model_fields:
            if field_name == 'raw':
                continue
            if field_name in row_dict:
                data[field_name] = row_dict[field_name]
            elif field_name in alias_values:
                data[field_name] = alias_values[field_name]
            elif field_name in lower_map:
                data[field_name] = lower_map[field_name]
        return VersionQueryResult(**data).model_dump()


    @staticmethod
    def _make_query_case_insensitive(sql_query: str) -> str:
        if not sql_query:
            return sql_query

        def _wrap_lower(column: str) -> str:
            normalized = column.strip()
            if normalized.lower().startswith('lower('):
                return normalized
            return f"LOWER({normalized})"

        def _replace_equals(match):
            column = match.group('column')
            value = match.group('value')
            return f"{_wrap_lower(column)} = LOWER('{value}')"

        equals_pattern = re.compile(r"(?P<column>[A-Za-z0-9_\.]+)\s*=\s*'(?P<value>[^']*)'", re.IGNORECASE)
        sql_query = equals_pattern.sub(_replace_equals, sql_query)

        def _replace_like(match):
            column = match.group('column')
            value = match.group('value')
            return f"{column} ILIKE '{value}'"

        like_pattern = re.compile(r"(?P<column>[A-Za-z0-9_\.]+)\s+LIKE\s+'(?P<value>[^']*)'", re.IGNORECASE)
        sql_query = like_pattern.sub(_replace_like, sql_query)

        def _replace_in(match):
            column = match.group('column')
            values = match.group('values')
            normalized_values = []
            for part in values.split(','):
                candidate = part.strip()
                if candidate.startswith("'") and candidate.endswith("'"):
                    normalized_values.append(f"LOWER({candidate})")
                else:
                    normalized_values.append(candidate)
            return f"{_wrap_lower(column)} IN ({', '.join(normalized_values)})"

        in_pattern = re.compile(r"(?P<column>[A-Za-z0-9_\.]+)\s+IN\s*\((?P<values>[^)]+)\)", re.IGNORECASE)
        sql_query = in_pattern.sub(_replace_in, sql_query)
        
        sql_query = sql_query.replace("\n", " ").replace("\r", " ")

        return sql_query
    
    @staticmethod
    def _enforce_select_all(sql_query: str) -> str:
        pattern = re.compile(r"SELECT\s+.+?\s+FROM\s+versions_enriched", re.IGNORECASE | re.DOTALL)
        return pattern.sub("SELECT * FROM versions_enriched", sql_query, count=1)

    

