import os

class Config:
    SQLALCHEMY_DATABASE_USER = os.getenv('POSTGRES_USER')
    SQLALCHEMY_DATABASE_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    SQLALCHEMY_DATABASE_NAME = os.getenv('POSTGRES_DB', 'whats-your-ride')
    SQLALCHEMY_DATABASE_PORT = os.getenv('POSTGRES_PORT', '5432')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')