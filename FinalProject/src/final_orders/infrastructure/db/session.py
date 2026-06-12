from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from final_orders.config.settings import settings

engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
