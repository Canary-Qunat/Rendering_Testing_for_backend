from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    id: UUID
    email: str
    password_hash: str
    is_active: bool
    created_at: datetime

    def deactivate(self) -> None:
        self.is_active = False

    def activate(self) -> None:
        self.is_active = True