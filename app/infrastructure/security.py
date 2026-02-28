from passlib.context import CryptContext
import secrets


_pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)

class PasswordHasher:
    def hash(self, password: str) -> str:
        return _pwd_context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return _pwd_context.verify(plain_password, hashed_password)


class TokenGenerator:
    def generate_secure_token(self) -> str:
        return secrets.token_urlsafe(64)