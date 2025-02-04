from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_order():
    response = client.post("/table_order/", json={"operation": "order", "table": 12, "waiter": 1})
    assert response.status_code == 200
    data = response.json()
    assert data['code'] == "212"

def test_order_small_code():
    response = client.post("/table_order/", json={"operation": "order", "table": 1, "waiter": 1})
    assert response.status_code == 200
    data = response.json()
    assert data['code'] == "201"