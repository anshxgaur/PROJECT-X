from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

# ==================== Base Schemas ====================

class CompanyBase(BaseModel):
    name: str
    registration_number: str
    address: str
    phone: str
    email: str

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TruckBase(BaseModel):
    registration_number: str
    model: str
    capacity_tons: float
    year_manufactured: int
    fuel_type: str

class TruckCreate(TruckBase):
    company_id: int

class TruckResponse(TruckBase):
    id: int
    company_id: int
    health_score: float
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DriverBase(BaseModel):
    name: str
    license_number: str
    phone: str
    email: str
    years_experience: int

class DriverCreate(DriverBase):
    company_id: int

class DriverResponse(DriverBase):
    id: int
    company_id: int
    accidents_count: int
    violations_count: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class RouteBase(BaseModel):
    origin_city: str
    destination_city: str
    distance_km: float
    avg_duration_hours: float
    highway_percentage: float

class RouteCreate(RouteBase):
    pass

class RouteResponse(RouteBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ==================== Bilty Schemas ====================

class BiltyStatusEnum(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DELAYED = "delayed"

class BiltyBase(BaseModel):
    bilty_number: str
    sender_name: str
    sender_address: str
    receiver_name: str
    receiver_address: str
    goods_description: str
    weight_kg: float
    rate_per_km: float

class BiltyCreate(BiltyBase):
    company_id: int
    route_id: int
    scheduled_pickup: datetime
    scheduled_delivery: datetime

class BiltyUpdate(BaseModel):
    status: Optional[BiltyStatusEnum] = None
    sender_name: Optional[str] = None
    receiver_name: Optional[str] = None
    goods_description: Optional[str] = None

class BiltyResponse(BiltyBase):
    id: int
    company_id: int
    route_id: int
    total_amount: float
    status: BiltyStatusEnum
    created_at: datetime
    scheduled_pickup: datetime
    scheduled_delivery: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ==================== Trip Schemas ====================

class TripBase(BaseModel):
    bilty_id: int
    truck_id: int
    driver_id: int

class TripCreate(TripBase):
    pass

class TripUpdate(BaseModel):
    current_location: Optional[str] = None
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None
    km_completed: Optional[float] = None
    delay_hours: Optional[float] = None
    notes: Optional[str] = None

class TripResponse(TripBase):
    id: int
    actual_start_time: Optional[datetime]
    actual_end_time: Optional[datetime]
    current_location: Optional[str]
    km_completed: float
    delay_hours: float
    delay_probability: float
    risk_level: str
    anomaly_score: float
    estimated_end_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TripDetailResponse(TripResponse):
    bilty: BiltyResponse
    truck: TruckResponse
    driver: DriverResponse

# ==================== ML Schemas ====================

class TripFeaturesSchema(BaseModel):
    distance_km: float = Field(..., description="Total distance in km")
    avg_duration_hours: float = Field(..., description="Average duration in hours")
    truck_health_score: float = Field(..., description="Truck health score 0-100")
    driver_experience_years: int = Field(..., description="Driver experience in years")
    weather_rain_mm: float = Field(..., description="Expected rainfall in mm")
    highway_percentage: float = Field(..., description="Highway percentage 0-100")
    weight_kg: float = Field(..., description="Cargo weight in kg")
    capacity_tons: float = Field(..., description="Truck capacity in tons")
    historical_delay_hours: float = Field(..., description="Historical delay for this route in hours")
    time_of_day: int = Field(..., description="Hour of day 0-23")
    is_monsoon: bool = Field(default=False, description="Is monsoon season")

class MLPredictionResponse(BaseModel):
    delay_probability: float = Field(..., description="Probability of delay 0-1")
    estimated_hours: float = Field(..., description="Estimated delay in hours")
    risk_level: str = Field(..., description="Risk level: green, yellow, orange, red")
    confidence: float = Field(..., description="Model confidence 0-1")

class SimulationOption(BaseModel):
    action: str  # "continue", "reroute", "hold"
    description: str
    estimated_impact: float
    risk_reduction: float

class SimulationResponse(BaseModel):
    trip_id: int
    current_risk: float
    options: List[SimulationOption]
    recommended: str

# ==================== Copilot Schemas ====================

class CopilotMessage(BaseModel):
    trip_id: int
    message: str
    context: Optional[dict] = None

class CopilotResponse(BaseModel):
    advice: str
    actions: List[str]
    priority: str  # "immediate", "urgent", "normal"

# ==================== Health Score Schemas ====================

class HealthScoreCalculation(BaseModel):
    truck_id: int
    age_years: float
    mileage_km: int
    days_since_service: int
    accident_history: int
    maintenance_score: float

class HealthScoreResponse(BaseModel):
    truck_id: int
    health_score: float
    rating: str  # "excellent", "good", "fair", "poor"
    risk_factors: List[str]
    recommendations: List[str]

# ==================== Cascade Risk Schemas ====================

class CascadeRiskResponse(BaseModel):
    trip_id: int
    affected_trip_id: Optional[int]
    risk_score: float
    impact_description: str

class CascadeAnalysisResponse(BaseModel):
    primary_risk: float
    cascade_risks: List[CascadeRiskResponse]
    total_network_impact: float
    affected_trips: int
