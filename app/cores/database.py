from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.cores.config import DATABASE_URL

print(f"Connecting to database: {DATABASE_URL}")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()