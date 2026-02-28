# This file contains the dependency for using the db

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.database import SessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session