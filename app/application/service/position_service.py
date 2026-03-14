from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from app.domain.entities.position import Position
from app.domain.interfaces.position_repo import PositionRepository


class PositionService:

    def __init__(self, position_repo: PositionRepository) -> None:
        self.position_repo = position_repo

    async def get_position(self, position_id: UUID) -> Position | None:
        return await self.position_repo.get_by_id(position_id)

    async def get_user_positions(self, user_id: UUID) -> list[Position]:
        return await self.position_repo.get_all_by_user(user_id)

    async def create_position(
        self,
        user_id: UUID,
        trading_symbol: str,
        exchange: str,
        quantity: int,
        avg_price: Decimal,
        last_price: Decimal,
        product: str,
        isin: str | None = None,
    ) -> Position:
        pnl = (last_price - avg_price) * quantity
        pnl_pct = ((last_price - avg_price) / avg_price) * 100 if avg_price else Decimal(0)

        position = Position(
            id=uuid4(),
            user_id=user_id,
            trading_symbol=trading_symbol,
            exchange=exchange,
            isin=isin,
            quantity=quantity,
            avg_price=avg_price,
            last_price=last_price,
            pnl=pnl,
            pnl_pct=pnl_pct,
            day_change=None,
            day_change_pct=None,
            product=product,
            synced_at=datetime.utcnow(),
        )
        return await self.position_repo.save(position)

    async def sync_market_data(
        self,
        position_id: UUID,
        last_price: Decimal,
        day_change: Decimal | None,
        day_change_pct: Decimal | None,
    ) -> Position | None:
        position = await self.position_repo.get_by_id(position_id)
        if not position:
            return None

        pnl = (last_price - position.avg_price) * position.quantity
        pnl_pct = ((last_price - position.avg_price) / position.avg_price) * 100

        position.update_market_data(
            last_price=last_price,
            pnl=pnl,
            pnl_pct=pnl_pct,
            day_change=day_change,
            day_change_pct=day_change_pct,
        )
        return await self.position_repo.update(position)

    async def delete_position(self, position_id: UUID) -> None:
        await self.position_repo.delete(position_id)