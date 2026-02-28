from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from app.domain.entities.refresh_token import RefreshToken


class RefreshTokenRepository(ABC):

    @abstractmethod
    def save(self, token: RefreshToken) -> None:
        pass

    @abstractmethod
    def get_by_token_hash(self, token_hash: str) -> Optional[RefreshToken]:
        pass

    @abstractmethod
    def revoke(self, token: RefreshToken) -> None:
        pass

    @abstractmethod
    def delete_by_user_id(self, user_id: UUID) -> None:
        pass