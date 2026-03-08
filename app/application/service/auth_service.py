from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from uuid import uuid4, UUID

from app.domain.entities.user import User
from app.domain.entities.refresh_token import RefreshToken
from app.domain.repositories.user_repo import UserRepository
from app.domain.repositories.refresh_token_repo import RefreshTokenRepository
from app.infrastructure.security import PasswordHasher, TokenGenerator
from app.infrastructure.jwt_service import JWTService
from app.infrastructure.settings import settings


@dataclass
class AuthTokens:
    access_token: str
    refresh_token: str


class AuthService:

    def __init__(
        self,
        user_repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository,
        password_hasher: PasswordHasher,
        jwt_service: JWTService,
        token_generator: TokenGenerator,
    ):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository
        self.password_hasher = password_hasher
        self.jwt_service = jwt_service
        self.token_generator = token_generator

    async def register_user(self, email: str, password: str) -> User:
        existing_user = await self.user_repository.get_by_email(email)

        if existing_user:
            raise ValueError("Email already registered")

        password_hash = self.password_hasher.hash(password)

        user = User(
            id=uuid4(),
            email=email,
            password_hash=password_hash,
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )

        await self.user_repository.save(user)

        return user

    async def login_user(self, email: str, password: str) -> AuthTokens:
        user = await self._validate_credentials(email, password)

        access_token = self.jwt_service.generate_access_token(user.id)

        refresh_token = self.token_generator.generate_secure_token()
        refresh_token_hash = self.password_hasher.hash(refresh_token)  #password and token hash are the same thing

        now = datetime.now(timezone.utc)

        refresh_entity = RefreshToken(
            id=uuid4(),
            user_id=user.id,
            token_hash=refresh_token_hash,
            expires_at=now + timedelta(days=settings.refresh_token_days),
            revoked=False,
            created_at=now,
        )

        await self.refresh_token_repository.save(refresh_entity)

        return AuthTokens(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def _validate_credentials(self, email: str, password: str) -> User:
        user = await self.user_repository.get_by_email(email)

        if user is None:
            raise ValueError("Invalid credentials")

        if not self.password_hasher.verify(password, user.password_hash):
            raise ValueError("Invalid credentials")

        if not user.is_active:
            raise ValueError("User inactive")

        return user

    async def logout(self, refresh_token: str, user_id: UUID) -> None:
        tokens = await self.refresh_token_repository.get_active_by_user_id(user_id)

        for token in tokens:
            if self.password_hasher.verify(refresh_token, token.token_hash):
                await self.refresh_token_repository.revoke(token)
                return

        raise ValueError("Invalid refresh token")