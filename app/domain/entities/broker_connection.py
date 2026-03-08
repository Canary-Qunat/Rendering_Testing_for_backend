from datetime import datetime
from uuid import UUID
from enum import Enum


class ConnectionStatus(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    EXPIRED = "expired"


class BrokerConnection:
    id: UUID
    user_id: UUID
    broker_name: str
    account_id: str

    access_token: str
    refresh_token: str
    expires_at: datetime

    status: ConnectionStatus

    created_at: datetime
    updated_at: datetime