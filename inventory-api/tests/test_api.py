from fastapi.testclient import TestClient
from app.main import create_app

def test_sell_and_stock():
    client = TestClient(create_app())
    product = client.post("/products", json={"name": "Mug", "stock": 5, "price_cents": 499}).json()
    sold = client.post(f"/products/{product['id']}/sell", json={"quantity": 2}).json()
    assert sold["remaining"] == 3
    assert client.post(f"/products/{product['id']}/sell", json={"quantity": 9}).status_code == 409
