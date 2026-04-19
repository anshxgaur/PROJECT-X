from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import (
    TripFeaturesSchema, MLPredictionResponse, HealthScoreCalculation, 
    HealthScoreResponse, CascadeAnalysisResponse, CascadeRiskResponse
)
from ml_pipeline import delay_predictor
from risk_engine import health_scorer, cascade_engine, anomaly_detector
from obsidian_reader import load_obsidian_bilties
import models

router = APIRouter(prefix="/api/ml", tags=["ML & Risk"])

@router.post("/predict", response_model=MLPredictionResponse)
def predict_delay(features: TripFeaturesSchema):
    """Predict delay probability for a trip using ML model"""
    
    features_dict = features.dict()
    prediction = delay_predictor.predict(features_dict)
    
    return MLPredictionResponse(
        delay_probability=prediction['delay_probability'],
        estimated_hours=prediction['estimated_hours'],
        risk_level=prediction['risk_level'],
        confidence=prediction['confidence']
    )

@router.post("/health-score", response_model=HealthScoreResponse)
def calculate_truck_health(calculation: HealthScoreCalculation, db: Session = Depends(get_db)):
    """Calculate truck health score"""
    
    truck_data = {
        'age_years': calculation.age_years,
        'mileage_km': calculation.mileage_km,
        'days_since_service': calculation.days_since_service,
        'accident_history': calculation.accident_history,
        'maintenance_score': calculation.maintenance_score
    }
    
    health_score = health_scorer.calculate_health_score(truck_data)
    rating = health_scorer.get_health_rating(health_score)
    risk_factors = health_scorer.get_risk_factors(truck_data)
    recommendations = health_scorer.get_recommendations(truck_data)
    
    # Update truck in database
    truck = db.query(models.Truck).filter(models.Truck.id == calculation.truck_id).first()
    if truck:
        truck.health_score = health_score
        db.commit()
    
    return HealthScoreResponse(
        truck_id=calculation.truck_id,
        health_score=health_score,
        rating=rating,
        risk_factors=risk_factors,
        recommendations=recommendations
    )

@router.post("/cascade-analysis/{trip_id}", response_model=CascadeAnalysisResponse)
def analyze_cascade_risk(trip_id: int, risk_score: float, db: Session = Depends(get_db)):
    """Analyze cascade risks for a trip"""
    
    # Get all active trips for graph building
    trips = db.query(models.Trip).all()
    trips_data = [
        {
            'id': t.id,
            'route_id': t.bilty.route_id if t.bilty else None,
            'risk_level': t.risk_level,
            'delay_probability': t.delay_probability
        }
        for t in trips
    ]
    
    # Build dependency graph
    cascade_engine.build_dependency_graph(trips_data)
    
    # Calculate cascade impact
    impact = cascade_engine.get_network_impact(trip_id, risk_score)
    
    # Convert to response format
    cascade_risks = [
        CascadeRiskResponse(
            trip_id=r['trip_id'],
            affected_trip_id=r['affected_trip_id'],
            risk_score=r['risk_score'],
            impact_description=r['impact_description']
        )
        for r in impact['cascade_risks']
    ]
    
    return CascadeAnalysisResponse(
        primary_risk=impact['primary_risk'],
        cascade_risks=cascade_risks,
        total_network_impact=impact['total_network_impact'],
        affected_trips=impact['affected_trips']
    )

@router.post("/anomaly-detection")
def detect_anomalies(db: Session = Depends(get_db)):
    """Detect anomalous trips using Isolation Forest"""
    
    import numpy as np
    
    # Get all trips with features
    trips = db.query(models.Trip).all()
    
    if len(trips) < 10:
        return {"message": "Need at least 10 trips for anomaly detection", "anomalies": []}
    
    # Extract features
    features = []
    trip_ids = []
    
    for trip in trips:
        features.append([
            trip.km_completed,
            trip.delay_hours,
            trip.delay_probability,
            trip.truck.health_score if trip.truck else 80,
            trip.driver.years_experience if trip.driver else 10
        ])
        trip_ids.append(trip.id)
    
    features_array = np.array(features)
    
    # Train and detect anomalies
    anomaly_detector.train(features_array)
    anomaly_scores = anomaly_detector.detect_anomalies(features_array)
    
    # Find anomalies
    anomalies = []
    for i, score in enumerate(anomaly_scores):
        if score > 0.7:  # Anomaly threshold
            anomalies.append({
                'trip_id': trip_ids[i],
                'anomaly_score': float(score),
                'severity': 'high' if score > 0.85 else 'medium'
            })
    
    return {'anomalies': anomalies, 'total_analyzed': len(trips)}


@router.get("/obsidian/bilties")
def get_obsidian_bilties():
    """Get all billing data from Obsidian vault"""
    try:
        bilties = load_obsidian_bilties('../obsidian_vault')
        return {
            'status': 'success',
            'count': len(bilties),
            'bilties': bilties
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading Obsidian bilties: {str(e)}")


@router.post("/predict-with-billing")
def predict_with_billing(features: TripFeaturesSchema):
    """Predict delay with billing impact analysis from Obsidian data"""
    try:
        features_dict = features.dict()
        
        # Load Obsidian bilties for context
        bilties = load_obsidian_bilties('../obsidian_vault')
        
        # Get prediction with billing features
        prediction = delay_predictor.predict(features_dict)
        
        # Add billing context if available
        matching_bilty = None
        if bilties:
            # Try to match with similar routes
            for bilty in bilties:
                if (abs(bilty['distance_km'] - features_dict.get('distance_km', 0)) < 100 and
                    bilty['origin_city'].lower() in str(features_dict).lower()):
                    matching_bilty = bilty
                    break
        
        return {
            'delay_probability': prediction['delay_probability'],
            'estimated_hours': prediction['estimated_hours'],
            'risk_level': prediction['risk_level'],
            'confidence': prediction['confidence'],
            'billing_impact': prediction.get('billing_impact', 'medium'),
            'billing_amount': prediction.get('billing_amount', 0),
            'priority_level': prediction.get('priority_level', 2),
            'matching_historical_bilty': matching_bilty,
            'trained_on_obsidian_data': True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in billing prediction: {str(e)}")


@router.get("/obsidian/bilty/{bilty_number}")
def get_bilty_details(bilty_number: str):
    """Get specific bilty details from Obsidian vault"""
    try:
        bilties = load_obsidian_bilties('../obsidian_vault')
        
        for bilty in bilties:
            if bilty['bilty_number'] == bilty_number:
                return {
                    'status': 'found',
                    'bilty': bilty
                }
        
        raise HTTPException(status_code=404, detail=f"Bilty {bilty_number} not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/obsidian/analytics")
def get_obsidian_analytics():
    """Get analytics from Obsidian billing data"""
    try:
        bilties = load_obsidian_bilties('../obsidian_vault')
        
        if not bilties:
            return {'status': 'no_data', 'message': 'No bilties found in Obsidian vault'}
        
        # Calculate analytics
        total_bilties = len(bilties)
        total_revenue = sum(b['total_amount'] for b in bilties)
        avg_delay = sum(b['actual_delay_hours'] for b in bilties) / total_bilties if total_bilties > 0 else 0
        
        # Risk distribution
        risk_distribution = {
            'completed': len([b for b in bilties if b['status'] == 'completed']),
            'active': len([b for b in bilties if b['status'] == 'active']),
            'delayed': len([b for b in bilties if b['status'] == 'delayed']),
            'pending': len([b for b in bilties if b['status'] == 'pending'])
        }
        
        # Priority distribution
        priority_dist = {
            'critical': len([b for b in bilties if b['priority'].lower() == 'critical']),
            'high': len([b for b in bilties if b['priority'].lower() == 'high']),
            'medium': len([b for b in bilties if b['priority'].lower() == 'medium']),
            'low': len([b for b in bilties if b['priority'].lower() == 'low'])
        }
        
        # Payment status
        payment_dist = {
            'paid': len([b for b in bilties if b['payment_status'].lower() == 'paid']),
            'pending': len([b for b in bilties if b['payment_status'].lower() == 'pending']),
            'partial': len([b for b in bilties if b['payment_status'].lower() == 'partial'])
        }
        
        return {
            'status': 'success',
            'total_bilties': total_bilties,
            'total_revenue': total_revenue,
            'average_delay_hours': avg_delay,
            'risk_distribution': risk_distribution,
            'priority_distribution': priority_dist,
            'payment_distribution': payment_dist,
            'data_source': 'Obsidian Vault'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating analytics: {str(e)}")
