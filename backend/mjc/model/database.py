from sqlmodel import create_engine

from backend.mjc.config import DATABASE_URL


engine = create_engine(DATABASE_URL)
