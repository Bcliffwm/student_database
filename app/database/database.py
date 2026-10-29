import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Database connection configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:////data/university.db"
)

# SQLite requires the parent directory to exist
if DATABASE_URL.startswith("sqlite:////data/"):
    os.makedirs("data", exist_ok=True)

# SQLite-specific connection arguments
connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass


# Dependency injection for FastAPI
def get_db():
    with SessionLocal() as session:
        yield session