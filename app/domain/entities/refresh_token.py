from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID


@dataclass
class RefreshToken:
    id: UUID
    user_id: UUID
    token_hash: str
    expires_at: datetime
    revoked: bool
    created_at: datetime

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc)>= self.expires_at

    def revoke(self) -> None:
        self.revoked = True

    def is_valid(self) -> bool:
        return not self.revoked and not self.is_expired()