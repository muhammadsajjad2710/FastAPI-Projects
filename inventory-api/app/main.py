from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

class ProductIn(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    stock: int = Field(ge=0)
    price_cents: int = Field(gt=0)

class SaleIn(BaseModel):
    quantity: int = Field(gt=0)

def create_app() -> FastAPI:
    app = FastAPI(title="Inventory API", version="1.0.0")
    app.state.products: dict[int, dict] = {}
    app.state.next_id = 1

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/products", status_code=201)
    def create_product(payload: ProductIn):
        product = {"id": app.state.next_id, **payload.model_dump()}
        app.state.next_id += 1
        app.state.products[product["id"]] = product
        return product

    @app.get("/products")
    def list_products():
        return list(app.state.products.values())

    @app.post("/products/{product_id}/sell")
    def sell(product_id: int, payload: SaleIn):
        product = app.state.products.get(product_id)
        if product is None:
            raise HTTPException(404, "Product not found")
        if product["stock"] < payload.quantity:
            raise HTTPException(409, "Insufficient stock")
        product["stock"] -= payload.quantity
        return {"sold": payload.quantity, "remaining": product["stock"]}

    return app

app = create_app()
