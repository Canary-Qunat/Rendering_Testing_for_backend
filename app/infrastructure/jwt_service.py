import jwt
from datetime import datetime, timezone, timedelta
from app.infrastructure.settings import settings

class JWTService:

    def __init__(self):
        self.secret_key = settings.jwt_secret_key
        self.algorithm = settings.jwt_algorithm
        self.access_token_minutes = settings.access_token_minutes

    def generate_access_token(self, user_id) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + timedelta(minutes=self.access_token_minutes),
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )