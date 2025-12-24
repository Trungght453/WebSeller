from fastapi import FastAPI
from app.api.v1 import auth, users, products, orders
from app.core.logging import setup_logging

def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title="Web Seller API",
        version="1.0.0",
    )

    app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
    app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
    app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
    app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app

# 🔴 THIS LINE IS REQUIRED
app = create_app()
