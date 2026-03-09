from app.domain.repositories.broker_connection_repo import BrokerConnectionRepository
from uuid import UUID
from datetime import datetime
from app.domain.entities.broker_connection import BrokerConnection

class PostgresBrokerConnectionRepository(BrokerConnectionRepository):
    def __init__(self, db):
        self.db = db

    async def get_by_user_id(self, user_id: UUID) -> BrokerConnection | None:
        query = """
            SELECT
                id,
                user_id,
                broker_name,
                account_id,
                access_token,
                refresh_token,
                expires_at,
                status,
                created_at,
                updated_at
            FROM broker_connections
            WHERE user_id = $1
            LIMIT 1
        """
        async with self.db.acquire() as conn:
            row = await conn.fetchrow(query, user_id)

        if not row:
            return None

        return BrokerConnection(**dict(row))

    async def get_active_by_user_id(self, user_id: UUID) -> BrokerConnection | None:
        query = """
            SELECT
                id,
                user_id,
                broker_name,
                account_id,
                access_token,
                refresh_token,
                expires_at,
                status,
                created_at,
                updated_at
            FROM broker_connectins
            WHERE user_id = $1
            AND status = 'connected'
            LIMIT 1
        """
        async with self.db.acquire() as conn:
            row = await conn.fetchrow(query, user_id)

        if not row:
            return None

        return BrokerConnection(**dict(row))

    async def save(self, connection: BrokerConnection) -> None:
        query = """
            INSERT INTO broker_connections (
                id,
                user_id,
                broker_name,
                account_id,
                access_token,
                refresh_token,
                expires_at,
                status,
                created_at,
                updated_at
            )
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
        """
        async with self.db.acquire() as conn:
            await conn.execute(
                query,
                connection.id,
                connection.user_id,
                connection.broker_name,
                connection.account_id,
                connection.access_token,
                connection.refresh_token,
                connection.expires_at,
                connection.status.value,
                connection.created_at,
                connection.updated_at,
            )

    async def update(self, connection: BrokerConnection) -> None:
        query = """
            UPDATE broker_connections
            SET
                broker_name = $1,
                account_id = $2,
                access_token = $3,
                refresh_token = $4,
                expires_at = $5,
                status = $6,
                updated_at = $7
            WHERE id = $8
        """
        async with self.db.acquire() as conn:
            await conn.execute(
                query,
                connection.broker_name,
                connection.account_id,
                connection.access_token,
                connection.refresh_token,
                connection.expires_at,
                connection.status.value,
                connection.updated_at,
                connection.id,
            )

    async def update_tokens(
            self,
            connection_id: UUID,
            access_token: str,
            refresh_token: str,
            expires_at: datetime,
    ) -> None:

        query = """
            UPDATE broker_connections
            SET
                access_token = $1,
                refresh_token = $2,
                expires_at = $3,
                updated_at = NOW()
            WHERE id = $4
        """
        async with self.db.acquire() as conn:
            await conn.execute(
                query,
                access_token,
                refresh_token,
                expires_at,
                connection_id,
            )

    async def delete(self, connection_id: UUID) -> None:
        query = """   
            DELETE FROM broker_connections   
            WHERE id = $1   
        """
        async with self.db.acquire() as conn:
            await conn.execute(query, connection_id)

