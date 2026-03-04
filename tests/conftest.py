import pytest
import asyncpg
import httpx

from app.main import create_app
from app.infrastructure.database import connection

TEST_DSN = "postgresql://user:password@localhost:5433/canary_test"


@pytest.fixture
async def client():
    app = create_app(use_lifespan=False)

    connection.db_pool = await asyncpg.create_pool(dsn=TEST_DSN)

    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        yield client

    await connection.db_pool.close()


@pytest.fixture(autouse=True)
async def clean_db():
    pool = await asyncpg.create_pool(dsn=TEST_DSN)

    async with pool.acquire() as conn:
        await conn.execute(
            "TRUNCATE refresh_tokens, users RESTART IDENTITY CASCADE;"
        )

    await pool.close()
