from uuid import UUID
from typing import Optional

from app.domain.entities.user import User
from app.domain.repositories.user_repo import UserRepository


class PostgresUserRepository(UserRepository):

    def __init__(self, db):
        self.db = db

    async def get_by_email(self, email: str) -> Optional[User]:
        query = """
            SELECT id, email, password_hash, is_active, created_at
            FROM users
            WHERE email = $1;
        """

        async with self.db.acquire() as conn:
            row = await conn.fetchrow(query, email)

        if row is None:
            return None

        return User(
            id=row["id"],
            email=row["email"],
            password_hash=row["password_hash"],
            is_active=row["is_active"],
            created_at=row["created_at"],
        )

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        query = """
            SELECT id, email, password_hash, is_active, created_at
            FROM users
            WHERE id = $1;
        """

        async with self.db.acquire() as conn:
            row = await conn.fetchrow(query, user_id)

        if row is None:
            return None

        return User(
            id=row["id"],
            email=row["email"],
            password_hash=row["password_hash"],
            is_active=row["is_active"],
            created_at=row["created_at"],
        )

    async def save(self, user: User) -> None:
        query = """
            INSERT INTO users (id, email, password_hash, is_active, created_at)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (id) DO UPDATE
            SET email = EXCLUDED.email,
                password_hash = EXCLUDED.password_hash,
                is_active = EXCLUDED.is_active;
        """

        async with self.db.acquire() as conn:
            await conn.execute(
                query,
                user.id,
                user.email,
                user.password_hash,
                user.is_active,
                user.created_at,
            )