import logging
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.db.session import engine
from app.core.logging import setup_logging

def check_db_connection():
    setup_logging()
    logger = logging.getLogger("db.check")

    logger.info("Checking database connection...")

    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT current_database(), current_user;")
            )
            db_name, db_user = result.fetchone()

            logger.info(
                "✅ Database connection SUCCESS | database=%s | user=%s",
                db_name,
                db_user,
            )

    except OperationalError:
        logger.exception("❌ Database connection FAILED (OperationalError)")
    except Exception:
        logger.exception("❌ Database connection FAILED (Unexpected error)")

if __name__ == "__main__":
    check_db_connection()
