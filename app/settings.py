import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_SOURCE = os.getenv("DB_SOURCE", "postgres")
    DB_USER = os.getenv("DB_USER", "user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_HOST = os.getenv("DB_HOST", "db")
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_NAME = os.getenv("DB_NAME", "mydatabase")
