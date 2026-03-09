from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from decimal import Decimal

@dataclass
class Positions:
    id : UUID
    user_id : UUID
    trading_symbol : str
    exchange : str
    quantity : int
    avg_price : Decimal
    last_price : Decimal
    pnl : Decimal
    pnl_percent : Decimal
    product : str
    synced_at : datetime

def update_market(self, last_price, pnl, pnl_percent) -> None:
    self.last_price = last_price
    self.pnl = pnl
    self.pnl_percent = pnl_percent
    self.synced_at = datetime.now()