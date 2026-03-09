from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.entities.positions import Positions

class PositionRespository(ABC):

    @abstractmethod
    async def  get_by_id(self, position_id: UUID) -> Positions | None:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all_by_user(self, user_id: UUID) -> list[Positions]:
        raise NotImplementedError
    
    @abstractmethod
    async def save(self, positions: Positions) -> Positions:
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, position:Positions) -> Positions:
        raise NotImplementedError