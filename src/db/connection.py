from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.model import Base

DATABASE_URL = "sqlite:///superstore.db"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
