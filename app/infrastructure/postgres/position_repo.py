from decimal import Decimal
from uuid import UUID

from app.domain.entities.positions import Positions
from app.domain.interfaces.positions_repo import PositionRespository
from app.infrastructure.database.connection import get_connection


class PostgresPositionRepository(PositionRespository):

    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def get_by_id(self, position_id: UUID) -> Positions | None:
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM positions WHERE id = $1",
                position_id,
            )
            if not row:
                return None
            return self._to_entity(row)


    async def get_all_by_user(self, user_id: UUID) -> list[Positions]:
        async with get_connection() as conn:
            rows = await conn.fetch(
                "SELECT * FROM positions WHERE user_id = $1",
                user_id,
            )
            return [self._to_entity(row) for row in rows]


    async def save(self, position: Positions) -> Positions:
        async with get_connection() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO positions(
                    id, user_id, trading_symbol, exchange,
                    quantity, avg_price, last_price, pnl, pnl_percent,
                    product, synced_at
                    ) VALUES(
                        $1, $2, $3, $4, $5,
                        $6, $7, $8, $9, $10,
                        $11) RETURNING *
                """,
                position.id, position.user_id, position.trading_symbol,
                position.exchange, position.quantity,
                position.avg_price, position.last_price, position.pnl,
                position.pnl_percent, position.product, position.synced_at,
            ) 
            return self._to_entity(row)
        
    async def update(self, position:Positions) -> Positions:
        async with get_connection() as conn:
            row = await conn.fetchrow(
                """
                UPDATE positions SET
                    last_price = $1, pnl = $2, pnl_percent=$3,synced_at = $4
                WHERE id = $5
                RETURNING *
                """,
                position.last_price, position.pnl, position.pnl_percent,
                position.synced_at, position.id,
            )
            return self._to_entity(row)
        
    async def delete(self, position_id: UUID) -> None:
        async with get_connection() as conn:
            await conn.execute(
                "DELETE FROM positions WHERE id = $1",
                position_id                    
            )
    
    @staticmethod
    def _to_entity(row) -> Positions:
        return Positions(
            id=row["id"],
            user_id=row["user_id"],
            trading_symbol=row["trading_symbol"],
            exchange=row["exchange"],
            quantity=row["quantity"],
            avg_price=Decimal(row["avg_price"]),
            last_price=Decimal(row["last_price"]),
            pnl=Decimal(row["pnl"]),
            pnl_percent=Decimal(row["pnl_percent"]),
            product=row["product"],
            synced_at=row["synced_at"]
        )