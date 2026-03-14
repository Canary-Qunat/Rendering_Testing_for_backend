import asyncpg
from app.infrastructure.settings import settings
from contextlib import asynccontextmanager

db_pool: asyncpg.Pool | None = None

async def connect_to_db() -> None:
    global db_pool

    db_pool = await asyncpg.create_pool(
        dsn=settings.database_url,
        min_size=5,
        max_size=20,
    )
@asyncontextmanager
async def get_connection():
    async with db_pool.acquire() as connection:
        yield connection

async def close_db_connection() -> None:
    global db_pool

    if db_pool:
        await db_pool.close()