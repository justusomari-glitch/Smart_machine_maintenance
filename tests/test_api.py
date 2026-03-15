from fastapi.testclient import TestClient
import src.prediction as prediction

client = TestClient(prediction.app)
def test_api_running():
    response = client.get("/")
    assert response.status_code == 200

def test_pediction_valid():
    payload = {
        "vibration_mm_s": 0.5,
        "temperature_c": 75.0,
        "load_percent": 80.0,
        "motor_current_amp": 10.0,
        "plant_section": "Kiln",
        "component": "Bearing",
        "sub_equipment": "Oil Pump",
        "major_equipment": "Crusher",
        "operating_hours": 10.0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data=response.json()
    assert "status" in data
    assert "maintenance_type" in data
    assert "days_to_next_failure" in data
    assert "failure_probability" in data
    assert "failure_message" in data

def test_prediction_invalid():
    bad_payload={
        "vibration_mm_s": 9.5,
        "temperature_c": 75.0,    
     }
    response = client.post("/predict", json=bad_payload)
    assert response.status_code == 422