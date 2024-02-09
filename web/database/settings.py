from sqlalchemy.ext.asyncio import create_async_engine
from decouple import config


username = config("POSTGRES_USER")
password = config("POSTGRES_PASSWORD")
host = config("POSTGRES_HOST")
dbname = config("POSTGRES_DB")


database_url: str = f"postgresql+asyncpg://{username}:{password}@{host}:5432/{dbname}"
engine = create_async_engine(str(database_url))
