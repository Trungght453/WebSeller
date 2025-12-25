from sqlalchemy import text
import uuid


def register_and_login(client, email: str, password: str = "123") -> str:
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )

    res = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )

    assert res.status_code == 200
    return res.json()["access_token"]


def insert_product(db, name: str, price: float, stock: int) -> int:
    result = db.execute(
        text("""
            INSERT INTO products (name, price, stock)
            VALUES (:name, :price, :stock)
            RETURNING id
        """),
        {"name": name, "price": price, "stock": stock},
    )
    product_id = result.scalar()
    db.commit()
    return product_id


def test_create_order_success(client, db):
    token = register_and_login(client, "order_success@test.com")

    product_id = insert_product(
        db,
        name=f"Tablet_{uuid.uuid4().hex[:6]}",
        price=300,
        stock=10,
    )

    res = client.post(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "items": [
                {"product_id": product_id, "quantity": 2}
            ]
        },
    )

    assert res.status_code == 200
    data = res.json()
    assert data["total_price"] == 600.0
    assert "order_id" in data


def test_order_without_auth_fails(client):
    res = client.post(
        "/api/v1/orders",
        json={
            "items": [
                {"product_id": 1, "quantity": 1}
            ]
        },
    )
    assert res.status_code == 401


def test_order_insufficient_stock(client, db):
    token = register_and_login(client, "order_stock_fail@test.com")

    product_id = insert_product(
        db,
        name=f"Phone_{uuid.uuid4().hex[:6]}",
        price=300,
        stock=1,
    )

    res = client.post(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "items": [
                {"product_id": product_id, "quantity": 2}
            ]
        },
    )

    assert res.status_code == 400
    assert "Not enough stock" in res.json()["detail"]
