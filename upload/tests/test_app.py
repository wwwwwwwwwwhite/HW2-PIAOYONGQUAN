from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def payload(**extra):
    data = {"budget": 1200000, "purpose": "game", "resolution": "1080p", "cpu_preference": "any", "gpu_preference": "any", "memory": 32, "storage": 1000}
    data.update(extra); return data

def test_recommendation_has_parts_and_total():
    response = client.post("/api/recommend", json=payload())
    assert response.status_code == 200
    body = response.json()
    assert len(body["parts"]) == 8
    assert body["total"] == sum(p["price"] for p in body["parts"])

def test_invalid_budget_is_rejected():
    assert client.post("/api/recommend", json=payload(budget=0)).status_code == 422

def test_front_page_loads():
    assert client.get("/").status_code == 200

def test_health_endpoint():
    assert client.get("/health").json()["status"] == "ok"

def test_optional_items_and_compatibility():
    body = client.post("/api/recommend", json=payload(include=["monitor", "keyboard"])).json()
    assert any(p["category"] == "모니터" for p in body["parts"])
    assert any(c["status"] == "확인" for c in body["compatibility"])

def test_missing_storage_data_is_reported():
    body = client.post("/api/recommend", json=payload(storage=2000)).json()
    assert body["warnings"]
