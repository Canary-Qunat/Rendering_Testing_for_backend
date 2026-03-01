from app.application.service.auth_service import AuthService
from app.infrastructure.postgres.user_repo import PostgresUserRepository
from app.infrastructure.postgres.refresh_token_repo import PostgresRefreshTokenRepository
from app.infrastructure.security import PasswordHasher, TokenGenerator
from app.infrastructure.jwt_service import JWTService
from app.infrastructure.database.connection import db_pool


#Infra
user_repo = PostgresUserRepository(db_pool)
refresh_repo = PostgresRefreshTokenRepository(db_pool)
password_hasher = PasswordHasher()
jwt_service = JWTService()
token_generator = TokenGenerator()

#Application
auth_service_instance = AuthService(
    user_repository=user_repo,
    refresh_token_repository=refresh_repo,
    password_hasher=password_hasher,
    jwt_service=jwt_service,
    token_generator=token_generator,
)

def get_auth_service() -> AuthService:
    return auth_service_instance