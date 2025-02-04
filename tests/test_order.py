from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_order():
    response = client.post("/table_order/", json={"operation": "order", "table": 12, "waiter": 1})
    assert response.status_code == 200
    data = response.json()
    assert data['code'] == "212"