from datetime import datetime
from typing import Protocol
from uuid import UUID
from app.domain.entities.broker_connection import BrokerConnection

class BrokerConnectionRepository(Protocol):

    async def get_by_user_id(self, user_id: UUID) -> BrokerConnection | None:
        ...

    async def get_active_by_user_id(self, user_id: UUID) -> BrokerConnection | None:
        ...

    async def save(self, connection: BrokerConnection) -> None:
        ...

    async def update(self, connection: BrokerConnection) -> None:
        ...

    async def update_tokens(
        self,
        connection_id: UUID,
        access_token: str,
        refresh_token: str,
        expires_at: datetime,
    ) -> None:
        ...

    async def delete(self, connection_id: UUID) -> None:
        ...