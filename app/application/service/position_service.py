from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from app.domain.entities.positions import Positions
from app.domain.interfaces.positions_repo import PositionRespository

class PositionService:

    def __init__(self, position_repo: PositionRespository) -> None:
        self.position_repo = position_repo
    
    async def get_positon(self, position_id: UUID) -> Positions | None:
        return await self.position_repo.get_by_id(position_id)
    
    async def get_user_position(self, user_id: UUID) -> list[Positions]:
        return await self.position_repo.get_all_by_user(user_id)
    
    async def create_position(
            self,
            user_id: UUID,
            trading_symbol: str,
            exchange: str,
            quantity: int,
            avg_price: Decimal,
            last_price: Decimal,
            product:str
    ) -> Positions:
        pnl = (last_price - avg_price) * quantity
        pnl_percent = ((last_price - avg_price)/ avg_price) * 100 if avg_price else Decimal(0)

        position = Positions(
            id = uuid4,
            user_id=user_id,
            trading_symbol=trading_symbol,
            exchange=exchange,
            quantity=quantity,
            avg_price=avg_price,
            last_price=last_price,
            pnl=pnl,
            pnl_percent = pnl_percent,
            product=product,
            synced_at=datetime.now(timezone.utc)
        )
        return await self.position_repo.save(position)
    
    async def sync_market_data(
            self,
            position_id: UUID,
            last_price: Decimal,
    ) -> Positions | None:
        position = await self.position_repo.get_by_id(position_id)
        if not position:
            return None
        
        pnl = (last_price - position.avg_price) * position.quantity
        pnl_percent = ((last_price - position.avg_price) / position.avg_price) * 100

        position.update_market_data(
            last_price=last_price,
            pnl=pnl,
            pnl_percent=pnl_percent,
        )

        return await self.position_repo.update(position=position)
    
    async def delete_position(self, position_id:UUID) -> None:
        await self.position_repo.delete(position_id)