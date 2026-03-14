from app.application.service.auth_service import AuthService
from app.infrastructure.postgres.user_repo import PostgresUserRepository
from app.infrastructure.postgres.refresh_token_repo import PostgresRefreshTokenRepository
from app.infrastructure.security import PasswordHasher, TokenGenerator
from app.infrastructure.jwt_service import JWTService
from app.infrastructure.database import connection
from app.application.service.position_service import PositionService
from app.infrastructure.postgres.position_repo import PositionRespository

def get_auth_service() -> AuthService:
    user_repo = PostgresUserRepository(connection.db_pool)
    refresh_repo = PostgresRefreshTokenRepository(connection.db_pool)

    password_hasher = PasswordHasher()
    jwt_service = JWTService()
    token_generator = TokenGenerator()

    return AuthService(
        user_repository=user_repo,
        refresh_token_repository=refresh_repo,
        password_hasher=password_hasher,
        jwt_service=jwt_service,
        token_generator=token_generator,
    )

def get_position_service() -> PositionService:
    position_Repo = PositionRespository(connection.db_pool)
    return PositionService(position_repo=position_Repo)