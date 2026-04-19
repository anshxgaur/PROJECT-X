from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
import models
from schemas import TripCreate, TripUpdate, TripResponse, TripDetailResponse

router = APIRouter(prefix="/api/trips", tags=["Trips"])

@router.post("", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    """Create a new trip"""
    # Verify bilty, truck, and driver exist
    bilty = db.query(models.Bilty).filter(models.Bilty.id == trip.bilty_id).first()
    if not bilty:
        raise HTTPException(status_code=404, detail="Bilty not found")
    
    truck = db.query(models.Truck).filter(models.Truck.id == trip.truck_id).first()
    if not truck:
        raise HTTPException(status_code=404, detail="Truck not found")
    
    driver = db.query(models.Driver).filter(models.Driver.id == trip.driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    # Create trip
    db_trip = models.Trip(
        bilty_id=trip.bilty_id,
        truck_id=trip.truck_id,
        driver_id=trip.driver_id,
        actual_start_time=datetime.utcnow()
    )
    
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

@router.get("", response_model=list[TripDetailResponse])
def get_trips(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all active trips"""
    trips = db.query(models.Trip).offset(skip).limit(limit).all()
    return trips

@router.get("/{trip_id}", response_model=TripDetailResponse)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    """Get trip by ID"""
    trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.put("/{trip_id}", response_model=TripResponse)
def update_trip(trip_id: int, trip_update: TripUpdate, db: Session = Depends(get_db)):
    """Update trip status"""
    db_trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    if trip_update.current_location:
        db_trip.current_location = trip_update.current_location
    if trip_update.current_lat:
        db_trip.current_lat = trip_update.current_lat
    if trip_update.current_lng:
        db_trip.current_lng = trip_update.current_lng
    if trip_update.km_completed is not None:
        db_trip.km_completed = trip_update.km_completed
    if trip_update.delay_hours is not None:
        db_trip.delay_hours = trip_update.delay_hours
    if trip_update.notes:
        db_trip.notes = trip_update.notes
    
    db_trip.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_trip)
    return db_trip

@router.get("/active/high-risk")
def get_high_risk_trips(db: Session = Depends(get_db)):
    """Get all high-risk trips (orange and red)"""
    trips = db.query(models.Trip).filter(
        models.Trip.risk_level.in_(["orange", "red"])
    ).all()
    return trips

@router.post("/{trip_id}/complete", response_model=TripResponse)
def complete_trip(trip_id: int, db: Session = Depends(get_db)):
    """Mark trip as completed"""
    db_trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    db_trip.actual_end_time = datetime.utcnow()
    db_trip.updated_at = datetime.utcnow()
    
    # Update bilty status
    bilty = db.query(models.Bilty).filter(models.Bilty.id == db_trip.bilty_id).first()
    if bilty:
        bilty.status = models.BiltyStatus.COMPLETED
        bilty.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_trip)
    return db_trip
