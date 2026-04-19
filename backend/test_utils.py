"""
Backend testing utilities
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from main import app
from database import Base, get_db
import models

# Test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)

def create_test_company(db):
    company = models.Company(
        name="Test Company",
        registration_number="TEST123",
        address="Test Address",
        phone="1234567890",
        email="test@test.com"
    )
    db.add(company)
    db.commit()
    return company

def create_test_truck(db, company_id):
    truck = models.Truck(
        registration_number="TEST-TRUCK-001",
        company_id=company_id,
        model="Test Truck",
        capacity_tons=20,
        year_manufactured=2020,
        fuel_type="Diesel",
        health_score=85.0
    )
    db.add(truck)
    db.commit()
    return truck

def create_test_driver(db, company_id):
    driver = models.Driver(
        name="Test Driver",
        company_id=company_id,
        license_number="LIC-001",
        phone="9876543210",
        email="driver@test.com",
        years_experience=10
    )
    db.add(driver)
    db.commit()
    return driver

def create_test_route(db):
    route = models.Route(
        origin_city="Delhi",
        destination_city="Mumbai",
        distance_km=1400,
        avg_duration_hours=22,
        highway_percentage=80
    )
    db.add(route)
    db.commit()
    return route

def create_test_bilty(db, company_id, route_id):
    bilty = models.Bilty(
        bilty_number="TEST-BILTY-001",
        company_id=company_id,
        route_id=route_id,
        sender_name="Test Sender",
        sender_address="Delhi",
        receiver_name="Test Receiver",
        receiver_address="Mumbai",
        goods_description="Test Goods",
        weight_kg=5000,
        rate_per_km=5.0,
        total_amount=7000,
        scheduled_pickup=datetime.utcnow(),
        scheduled_delivery=datetime.utcnow() + timedelta(hours=24)
    )
    db.add(bilty)
    db.commit()
    return bilty

def create_test_trip(db, bilty_id, truck_id, driver_id):
    trip = models.Trip(
        bilty_id=bilty_id,
        truck_id=truck_id,
        driver_id=driver_id,
        actual_start_time=datetime.utcnow(),
        delay_probability=0.2,
        risk_level="green"
    )
    db.add(trip)
    db.commit()
    return trip
