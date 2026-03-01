from fastapi import APIRouter, Depends, HTTPException, status
from app.application.service.auth_service import AuthService
from app.domain.entities.user import User
from app.presentation.schemas.auth_schemas import RegisterRequest, LoginRequest, TokenResponse, UserResponse, LogoutRequest
from app.infrastructure.dependencies.services import get_auth_service
from app.infrastructure.dependencies.auth import get_current_user


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(
    request: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        user = await auth_service.register_user(
            email=request.email,
            password=request.password,
        )
        return user

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        tokens = await auth_service.login_user(
            email=request.email,
            password=request.password,
        )
        return tokens

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

from uuid import UUID


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: LogoutRequest,
    user_id: UUID,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        await auth_service.logout(
            refresh_token=request.refresh_token,
            user_id=user_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me", response_model=UserResponse)
async def me(
    current_user: User = Depends(get_current_user),
):
    return current_user