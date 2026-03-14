from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from app.application.service.position_service import PositionService
from app.domain.entities.user import User
from app.infrastructure.dependencies.auth import get_current_user
from app.infrastructure.dependencies.services import get_position_service
from app.presentation.schemas.position_schema import(
    CreatePositionRequest,
    PositionResponse,
    SyncMarketDataRequest,
)

router = APIRouter(prefix="/positions", tags=["positions"])

@router.get("/",response_model=list[PositionResponse])
async def list_positions(
    current_user: User = Depends(get_current_user),
    position_service: PositionService = Depends(get_position_service)
):
    return await position_service.get_user_position(current_user.id)

@router.get("/{position_id}", response_model=PositionResponse)
async def get_position(
    position_id: UUID,
    current_user: User = Depends(get_current_user),
    position_service: PositionService = Depends(get_position_service),
):
    position = await position_service.get_position(position_id)
    if not position or position.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Position not found")
    return position
 
 
@router.post("/", response_model=PositionResponse, status_code=status.HTTP_201_CREATED)
async def create_position(
    body: CreatePositionRequest,
    current_user: User = Depends(get_current_user),
    position_service: PositionService = Depends(get_position_service),
):
    return await position_service.create_position(
        user_id=current_user.id,
        trading_symbol=body.trading_symbol,
        exchange=body.exchange,
        quantity=body.quantity,
        avg_price=body.avg_price,
        last_price=body.last_price,
        product=body.product,
        isin=body.isin,
    )
 
 
@router.patch("/{position_id}/sync", response_model=PositionResponse)
async def sync_market_data(
    position_id: UUID,
    body: SyncMarketDataRequest,
    current_user: User = Depends(get_current_user),
    position_service: PositionService = Depends(get_position_service),
):
    position = await position_service.sync_market_data(
        position_id=position_id,
        last_price=body.last_price,
        day_change=body.day_change,
        day_change_pct=body.day_change_pct,
    )
    if not position or position.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Position not found")
    return position
 
 
@router.delete("/{position_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_position(
    position_id: UUID,
    current_user: User = Depends(get_current_user),
    position_service: PositionService = Depends(get_position_service),
):
    position = await position_service.get_position(position_id)
    if not position or position.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Position not found")
    await position_service.delete_position(position_id)
 