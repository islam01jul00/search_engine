from dotenv import load_dotenv

load_dotenv()

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

DATABASE_URL = getenv("DATABASE_URL")

# Make sure your URL starts with `postgresql+asyncpg://`
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

async_session_maker = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

sync_engine = create_engine(DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://"), echo=False)