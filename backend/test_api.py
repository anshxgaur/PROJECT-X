"""
Test suite for BiltyBook Intelligence API
Run with: pytest test_api.py
"""

import pytest
from test_utils import client, db, create_test_company, create_test_truck, create_test_driver, create_test_route, create_test_bilty, create_test_trip

class TestHealth:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "OK"

    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "BiltyBook Intelligence" in response.json()["name"]

class TestDemoData:
    def test_init_demo_data(self):
        response = client.post("/api/demo/init")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["summary"]["companies"] == 1
        assert data["summary"]["trucks"] == 2

class TestTrips:
    def test_get_trips(self):
        # Initialize demo data first
        client.post("/api/demo/init")
        
        response = client.get("/api/trips")
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_get_trip_by_id(self):
        client.post("/api/demo/init")
        
        # Get first trip
        trips = client.get("/api/trips").json()
        if trips:
            trip_id = trips[0]["id"]
            response = client.get(f"/api/trips/{trip_id}")
            assert response.status_code == 200
            assert response.json()["id"] == trip_id

class TestMLPrediction:
    def test_predict_delay(self):
        features = {
            "distance_km": 1400,
            "avg_duration_hours": 22,
            "truck_health_score": 85,
            "driver_experience_years": 12,
            "weather_rain_mm": 10,
            "highway_percentage": 80,
            "weight_kg": 5000,
            "capacity_tons": 20,
            "historical_delay_hours": 1.5,
            "time_of_day": 14,
            "is_monsoon": False
        }
        
        response = client.post("/api/ml/predict", json=features)
        assert response.status_code == 200
        
        data = response.json()
        assert "delay_probability" in data
        assert "estimated_hours" in data
        assert "risk_level" in data
        assert 0 <= data["delay_probability"] <= 1
        assert data["risk_level"] in ["green", "yellow", "orange", "red"]

class TestSimulation:
    def test_simulation_endpoint(self):
        # Initialize demo data
        client.post("/api/demo/init")
        
        # Get a trip
        trips = client.get("/api/trips").json()
        if trips:
            trip_id = trips[0]["id"]
            response = client.post(f"/api/simulation/{trip_id}")
            assert response.status_code == 200
            
            data = response.json()
            assert "trip_id" in data
            assert "current_risk" in data
            assert "options" in data
            assert "recommended" in data

class TestCopilot:
    def test_copilot_chat(self):
        # Initialize demo data
        client.post("/api/demo/init")
        
        # Get a trip
        trips = client.get("/api/trips").json()
        if trips:
            trip_id = trips[0]["id"]
            
            response = client.post("/api/copilot/chat", json={
                "trip_id": trip_id,
                "message": "What should I do about this trip?"
            })
            
            assert response.status_code == 200
            data = response.json()
            assert "advice" in data
            assert "actions" in data
            assert "priority" in data
