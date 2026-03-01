from uuid import UUID
from typing import List
from app.domain.entities.refresh_token import RefreshToken
from app.domain.interfaces.refresh_token_repo import RefreshTokenRepository


class PostgresRefreshTokenRepository(RefreshTokenRepository):

    def __init__(self, db):
        self.db = db

    async def save(self, refresh_token: RefreshToken) -> None:
        query = """
            INSERT INTO refresh_tokens (
                id,
                user_id,
                token_hash,
                expires_at,
                revoked,
                created_at
            )
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (id) DO UPDATE
            SET token_hash = EXCLUDED.token_hash,
                expires_at = EXCLUDED.expires_at,
                revoked = EXCLUDED.revoked;
        """

        async with self.db.acquire() as conn:
            await conn.execute(
                query,
                refresh_token.id,
                refresh_token.user_id,
                refresh_token.token_hash,
                refresh_token.expires_at,
                refresh_token.revoked,
                refresh_token.created_at,
            )

    async def get_active_by_user_id(self, user_id: UUID) -> List[RefreshToken]:
        query = """
            SELECT id, user_id, token_hash, expires_at, revoked, created_at
            FROM refresh_tokens
            WHERE user_id = $1
              AND revoked = false
              AND expires_at > NOW();
        """

        async with self.db.acquire() as conn:
            rows = await conn.fetch(query, user_id)

        return [
            RefreshToken(
                id=row["id"],
                user_id=row["user_id"],
                token_hash=row["token_hash"],
                expires_at=row["expires_at"],
                revoked=row["revoked"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    async def revoke(self, token: RefreshToken) -> None:
        query = """
            UPDATE refresh_tokens
            SET revoked = true
            WHERE id = $1;
        """

        async with self.db.acquire() as conn:
            await conn.execute(query, token.id)

    async def delete_by_user_id(self, user_id: UUID) -> None:
        query = """
            DELETE FROM refresh_tokens
            WHERE user_id = $1;
        """

        async with self.db.acquire() as conn:
            await conn.execute(query, user_id)
