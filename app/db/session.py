from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


##tempt for lgogging database URL loading
from app.core.config import settings
import logging

logger = logging.getLogger("db.session")

logger.info(
    "DATABASE_URL loaded from env (masked): %s",
    settings.DATABASE_URL.replace(settings.DATABASE_URL.split("@")[0], "***")
)
