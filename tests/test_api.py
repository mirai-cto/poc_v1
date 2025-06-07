from fastapi.testclient import TestClient
from neurmill_poc_py.main import app

client = TestClient(app)

def test_get_machines():
    """
    Test the /machines endpoint to ensure it returns a list of machines.
    """
    response = client.get("/machines")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    # Optional: check for expected keys if DB has at least one machine
    if data:
        machine = data[0]
        assert "id" in machine
        assert "title" in machine           # 🔄 was 'name'
        assert "description" in machine
        assert "product_link" in machine
        assert "max_rpm" in machine         # ✅ still here (from parsed JSON)
        assert "max_power" in machine       # ✅ still here (from parsed JSON)

def test_dummy():
    assert 1 + 1 == 2
