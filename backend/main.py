from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uvicorn
import os

# Import database and models
from database import init_db, get_db, engine, Base
import models

# Import routers
from routers import bilty, trip, ml, copilot

# Initialize FastAPI app
app = FastAPI(
    title="BiltyBook Intelligence API",
    description="Real-time AI-powered truck transportation platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
def startup():
    """Initialize database on startup"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized")

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "OK", "timestamp": datetime.utcnow()}

# Root endpoint
@app.get("/")
def root():
    """API root endpoint"""
    return {
        "name": "BiltyBook Intelligence",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "features": [
            "Real-time trip tracking",
            "ML-based delay prediction",
            "Cascade risk analysis",
            "Truck health scoring",
            "AI copilot assistance",
            "Decision simulation"
        ]
    }

# Include routers
app.include_router(bilty.router)
app.include_router(trip.router)
app.include_router(ml.router)
app.include_router(copilot.router)

# ==================== Demo Data Endpoints ====================

@app.post("/api/demo/init")
def initialize_demo_data(db: Session = Depends(get_db)):
    """Initialize demo data for testing"""
    try:
        # Clear existing data
        db.query(models.Trip).delete()
        db.query(models.Bilty).delete()
        db.query(models.Driver).delete()
        db.query(models.Truck).delete()
        db.query(models.Route).delete()
        db.query(models.Company).delete()
        db.commit()
        
        # Create sample company
        company = models.Company(
            name="Elite Transport Co.",
            registration_number="REG123456",
            address="123 Transport Hub, Delhi",
            phone="+91-9876543210",
            email="info@elitetransport.com"
        )
        db.add(company)
        db.flush()
        
        # Create sample trucks
        trucks = [
            models.Truck(
                registration_number="DL-01-AB-0001",
                company_id=company.id,
                model="Tata 3120 Truck",
                capacity_tons=20,
                year_manufactured=2020,
                fuel_type="Diesel",
                last_service_date=datetime.utcnow() - timedelta(days=15),
                mileage_km=150000,
                health_score=92.0
            ),
            models.Truck(
                registration_number="DL-01-AB-0002",
                company_id=company.id,
                model="Ashok Leyland 2520",
                capacity_tons=25,
                year_manufactured=2019,
                fuel_type="Diesel",
                last_service_date=datetime.utcnow() - timedelta(days=45),
                mileage_km=220000,
                health_score=78.5
            )
        ]
        db.add_all(trucks)
        db.flush()
        
        # Create sample drivers
        drivers = [
            models.Driver(
                name="Rajesh Kumar",
                company_id=company.id,
                license_number="DL-LIC-001",
                phone="+91-9123456789",
                email="rajesh@elitetransport.com",
                years_experience=12,
                accidents_count=0
            ),
            models.Driver(
                name="Suresh Singh",
                company_id=company.id,
                license_number="DL-LIC-002",
                phone="+91-9987654321",
                email="suresh@elitetransport.com",
                years_experience=8,
                accidents_count=1
            )
        ]
        db.add_all(drivers)
        db.flush()
        
        # Create sample routes
        routes = [
            models.Route(
                origin_city="Delhi",
                destination_city="Mumbai",
                distance_km=1400,
                avg_duration_hours=22,
                highway_percentage=80
            ),
            models.Route(
                origin_city="Delhi",
                destination_city="Bangalore",
                distance_km=2200,
                avg_duration_hours=36,
                highway_percentage=75
            ),
            models.Route(
                origin_city="Mumbai",
                destination_city="Pune",
                distance_km=150,
                avg_duration_hours=3,
                highway_percentage=90
            )
        ]
        db.add_all(routes)
        db.flush()
        
        # Create sample bilties
        bilties = [
            models.Bilty(
                bilty_number="BL-001-2024",
                company_id=company.id,
                route_id=routes[0].id,
                sender_name="ABC Manufacturing",
                sender_address="Okhla Industrial Area, Delhi",
                receiver_name="XYZ Retailer",
                receiver_address="BKC, Mumbai",
                goods_description="Electronic components",
                weight_kg=5000,
                rate_per_km=5.5,
                total_amount=7700,
                status=models.BiltyStatus.ACTIVE,
                scheduled_pickup=datetime.utcnow() + timedelta(hours=1),
                scheduled_delivery=datetime.utcnow() + timedelta(hours=25)
            ),
            models.Bilty(
                bilty_number="BL-002-2024",
                company_id=company.id,
                route_id=routes[2].id,
                sender_name="Quick Logistics",
                sender_address="Navi Mumbai",
                receiver_name="Local Distributor",
                receiver_address="Pune Market",
                goods_description="Packaged goods",
                weight_kg=8000,
                rate_per_km=6.0,
                total_amount=900,
                status=models.BiltyStatus.PENDING,
                scheduled_pickup=datetime.utcnow() + timedelta(hours=2),
                scheduled_delivery=datetime.utcnow() + timedelta(hours=5)
            )
        ]
        db.add_all(bilties)
        db.flush()
        
        # Create sample trips
        trips = [
            models.Trip(
                bilty_id=bilties[0].id,
                truck_id=trucks[0].id,
                driver_id=drivers[0].id,
                actual_start_time=datetime.utcnow(),
                current_location="Delhi",
                km_completed=0,
                delay_probability=0.15,
                risk_level="green",
                estimated_end_time=datetime.utcnow() + timedelta(hours=22)
            ),
            models.Trip(
                bilty_id=bilties[1].id,
                truck_id=trucks[1].id,
                driver_id=drivers[1].id,
                actual_start_time=datetime.utcnow() + timedelta(hours=1),
                current_location="Navi Mumbai",
                km_completed=50,
                delay_probability=0.55,
                risk_level="orange",
                estimated_end_time=datetime.utcnow() + timedelta(hours=5)
            )
        ]
        db.add_all(trips)
        db.commit()
        
        return {
            "status": "success",
            "message": "Demo data initialized",
            "summary": {
                "companies": 1,
                "trucks": len(trucks),
                "drivers": len(drivers),
                "routes": len(routes),
                "bilties": len(bilties),
                "trips": len(trips)
            }
        }
    
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}

# Error handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000))
    )
