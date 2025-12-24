from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from app.models.product import Product
from app.models.order import Order, OrderItem
from app.models.user import User


def create_order(
    db: Session,
    user: User,
    items: list[dict],
) -> Order:
    """
    Create an order atomically with concurrency protection.
    """

    if not items:
        raise HTTPException(status_code=400, detail="Order must have items")

    total_price = 0.0
    order_items: list[OrderItem] = []

    for item in items:
        product = (
            db.execute(
                select(Product)
                .where(Product.id == item["product_id"])
                .with_for_update()   # 🔒 ROW LOCK
            )
            .scalar_one_or_none()
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item['product_id']} not found",
            )

        if product.stock < item["quantity"]:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {product.name}",
            )

        # mutate shared state safely
        product.stock -= item["quantity"]

        line_price = float(product.price) * item["quantity"]
        total_price += line_price

        order_items.append(
            OrderItem(
                product_id=product.id,
                quantity=item["quantity"],
                price=product.price,
            )
        )

    order = Order(
        user_id=user.id,
        status="pending",
        total_price=total_price,
        items=order_items,
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order
