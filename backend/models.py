from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum, JSON
from sqlalchemy.orm import relationship
from database import Base
import enum

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    registration_number = Column(String(100), unique=True)
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    trucks = relationship("Truck", back_populates="company", cascade="all, delete-orphan")
    drivers = relationship("Driver", back_populates="company", cascade="all, delete-orphan")
    bilties = relationship("Bilty", back_populates="company", cascade="all, delete-orphan")

class Truck(Base):
    __tablename__ = "trucks"
    
    id = Column(Integer, primary_key=True, index=True)
    registration_number = Column(String(50), unique=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), index=True)
    model = Column(String(100))
    capacity_tons = Column(Float)
    year_manufactured = Column(Integer)
    fuel_type = Column(String(50))
    last_service_date = Column(DateTime)
    mileage_km = Column(Integer)
    health_score = Column(Float, default=100.0)  # 0-100
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company = relationship("Company", back_populates="trucks")
    trips = relationship("Trip", back_populates="truck")

class Driver(Base):
    __tablename__ = "drivers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), index=True)
    license_number = Column(String(50), unique=True)
    phone = Column(String(20))
    email = Column(String(100))
    years_experience = Column(Integer)
    accidents_count = Column(Integer, default=0)
    violations_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company = relationship("Company", back_populates="drivers")
    trips = relationship("Trip", back_populates="driver")

class Route(Base):
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    origin_city = Column(String(100), index=True)
    destination_city = Column(String(100), index=True)
    distance_km = Column(Float)
    avg_duration_hours = Column(Float)
    highway_percentage = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    bilties = relationship("Bilty", back_populates="route")

class BiltyStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DELAYED = "delayed"

class Bilty(Base):
    __tablename__ = "bilties"
    
    id = Column(Integer, primary_key=True, index=True)
    bilty_number = Column(String(50), unique=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), index=True)
    route_id = Column(Integer, ForeignKey("routes.id"), index=True)
    sender_name = Column(String(100))
    sender_address = Column(Text)
    receiver_name = Column(String(100))
    receiver_address = Column(Text)
    goods_description = Column(Text)
    weight_kg = Column(Float)
    rate_per_km = Column(Float)
    total_amount = Column(Float)
    status = Column(Enum(BiltyStatus), default=BiltyStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    scheduled_pickup = Column(DateTime)
    scheduled_delivery = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company = relationship("Company", back_populates="bilties")
    route = relationship("Route", back_populates="bilties")
    trips = relationship("Trip", back_populates="bilty", cascade="all, delete-orphan")

class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True, index=True)
    bilty_id = Column(Integer, ForeignKey("bilties.id"), index=True)
    truck_id = Column(Integer, ForeignKey("trucks.id"), index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), index=True)
    actual_start_time = Column(DateTime, nullable=True)
    actual_end_time = Column(DateTime, nullable=True)
    current_location = Column(String(100), nullable=True)
    current_lat = Column(Float, nullable=True)
    current_lng = Column(Float, nullable=True)
    km_completed = Column(Float, default=0.0)
    delay_hours = Column(Float, default=0.0)
    delay_probability = Column(Float, default=0.0)  # ML prediction
    risk_level = Column(String(20), default="green")  # green, yellow, orange, red
    anomaly_score = Column(Float, default=0.0)  # Isolation Forest score
    estimated_end_time = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    bilty = relationship("Bilty", back_populates="trips")
    truck = relationship("Truck", back_populates="trips")
    driver = relationship("Driver", back_populates="trips")
    cascade_risks = relationship("CascadeRisk", back_populates="trip", cascade="all, delete-orphan")

class CascadeRisk(Base):
    __tablename__ = "cascade_risks"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), index=True)
    affected_trip_id = Column(Integer, nullable=True)
    risk_score = Column(Float)
    impact_description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    trip = relationship("Trip", back_populates="cascade_risks")

class MLPrediction(Base):
    __tablename__ = "ml_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=True)
    delay_probability = Column(Float)
    estimated_hours = Column(Float)
    risk_level = Column(String(20))
    input_features = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
