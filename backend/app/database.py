from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from supabase import create_client, Client
from app.config import settings

# SQLAlchemy (for local migrations if needed)
engine = create_engine("postgresql://localhost/data_agent")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Supabase client
supabase: Client = create_client(settings.supabase_url, settings.supabase_key)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()