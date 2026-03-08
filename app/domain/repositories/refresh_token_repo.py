from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from app.domain.entities.refresh_token import RefreshToken


class RefreshTokenRepository(ABC):

    @abstractmethod
    async def save(self, token: RefreshToken) -> None:
        pass

    @abstractmethod
    async def revoke(self, token: RefreshToken) -> None:
        pass

    @abstractmethod
    async def delete_by_user_id(self, user_id: UUID) -> None:
        pass

    @abstractmethod
    async def get_active_by_user_id(self, user_id: UUID) -> List[RefreshToken]:
        pass
