from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_paid():
    response = client.post("/table_order/", json={"operation": "paid", "table": 12, "waiter": 1})
    assert response.status_code == 200
    data = response.json()
    assert data['code'] == "012"

def test_paid_small_code():
    response = client.post("/table_order/", json={"operation": "order", "table": 1, "waiter": 1})
    assert response.status_code == 200
    data = response.json()
    assert data['code'] == "201"