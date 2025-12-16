from sqlalchemy import URL, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import Config

DATABASE_URL = URL.create(
    drivername='postgresql+psycopg2',
    username=Config.DB_USER,
    password=Config.DB_PASS,
    host=Config.DB_HOST,
    port=Config.DB_PORT,
    database=Config.DB_NAME
)

engine = create_engine(url=DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
