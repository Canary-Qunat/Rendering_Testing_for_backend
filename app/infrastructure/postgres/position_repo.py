from decimal import Decimal
from uuid import UUID

from app.domain.entities.positions import Positions
from app.domain.interfaces.positions_repo import PositionRespository
from app.infrastructure.database.connection import get_connection


