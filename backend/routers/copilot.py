from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import CopilotMessage, CopilotResponse, SimulationResponse, SimulationOption
from copilot_engine import copilot_engine, generate_simulation_cards
import models

router = APIRouter(prefix="/api", tags=["Copilot & Simulation"])

@router.post("/copilot/chat", response_model=CopilotResponse)
def copilot_chat(msg: CopilotMessage, db: Session = Depends(get_db)):
    """Chat with AI logistics copilot"""
    
    # Get trip details
    trip = db.query(models.Trip).filter(models.Trip.id == msg.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Build context
    trip_context = {
        'trip_id': trip.id,
        'origin': trip.bilty.route.origin_city if trip.bilty and trip.bilty.route else 'Unknown',
        'destination': trip.bilty.route.destination_city if trip.bilty and trip.bilty.route else 'Unknown',
        'distance_km': trip.bilty.route.distance_km if trip.bilty and trip.bilty.route else 0,
        'truck_model': trip.truck.model if trip.truck else 'Unknown',
        'truck_health': trip.truck.health_score if trip.truck else 80,
        'driver_experience': trip.driver.years_experience if trip.driver else 5,
        'delay_probability': trip.delay_probability,
        'estimated_delay_hours': trip.delay_hours
    }
    
    # Query copilot
    response = copilot_engine.query_copilot(
        trip_context=trip_context,
        risk_level=trip.risk_level,
        message=msg.message
    )
    
    return CopilotResponse(
        advice=response['advice'],
        actions=response['actions'],
        priority=response['priority']
    )

@router.post("/simulation/{trip_id}", response_model=SimulationResponse)
def simulate_trip_options(trip_id: int, db: Session = Depends(get_db)):
    """Generate simulation cards for decision support"""
    
    trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Build trip data
    trip_data = {
        'trip_id': trip.id,
        'truck_health': trip.truck.health_score if trip.truck else 80,
        'current_delay': trip.delay_hours,
        'delay_probability': trip.delay_probability
    }
    
    # Generate simulation options
    current_risk = trip.delay_probability
    options_data = generate_simulation_cards(trip_data, current_risk)
    
    # Determine recommended action
    recommended = 'continue'
    if current_risk > 0.6:
        recommended = 'reroute'
    elif current_risk > 0.4:
        recommended = 'hold'
    
    # Convert to response format
    options = [
        SimulationOption(
            action=opt['action'],
            description=opt['description'],
            estimated_impact=opt['estimated_impact'],
            risk_reduction=opt['risk_reduction']
        )
        for opt in options_data
    ]
    
    return SimulationResponse(
        trip_id=trip_id,
        current_risk=current_risk,
        options=options,
        recommended=recommended
    )
