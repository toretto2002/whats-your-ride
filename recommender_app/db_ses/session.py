from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Engine per LlamaIndex, separato dal context Flask
llama_engine = create_engine(DATABASE_URL)
llama_session = sessionmaker(bind=llama_engine)
