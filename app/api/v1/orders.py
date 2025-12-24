from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import create_order
from app.api.deps import get_current_user
from app.db.session import get_db

router = APIRouter()


@router.post("/", response_model=OrderResponse)
def place_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    order = create_order(
        db=db,
        user=user,
        items=[item.model_dump() for item in payload.items],
    )

    return {
        "order_id": order.id,
        "total_price": float(order.total_price),
    }
