import pytest
import asyncpg

TEST_DSN = "postgresql://user:password@localhost:5433/canary_test"


@pytest.mark.asyncio
async def test_db_connection():
    pool = await asyncpg.create_pool(dsn=TEST_DSN)

    async with pool.acquire() as conn:
        result = await conn.fetchval("SELECT 1;")
        assert result == 1

    await pool.close()


@pytest.mark.asyncio
async def test_correct_database():
    pool = await asyncpg.create_pool(dsn=TEST_DSN)

    async with pool.acquire() as conn:
        db_name = await conn.fetchval("SELECT current_database();")
        assert db_name == "canary_test"

    await pool.close()