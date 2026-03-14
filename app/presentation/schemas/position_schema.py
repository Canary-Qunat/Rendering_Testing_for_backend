from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

class CreatePositionRequest(BaseModel):
    trading_symbol : str
    exchange : str
    quantity : int
    avg_price : Decimal
    last_price : Decimal
    product : str

class SyncMarketDataRequest(BaseModel):
    last_price : Decimal

class PositionResponse(BaseModel):
    id : UUID
    user_id : UUID
    trading_symbol : str
    exchange : str
    avg_price : Decimal
    last_price : Decimal
    pnl : Decimal
    pnl_percent : Decimal
    product : str
    synced_at : datetime

    class Config:
        from_attribute = True
        