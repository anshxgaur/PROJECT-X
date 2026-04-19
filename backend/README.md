# BiltyBook Intelligence - Backend

AI-powered real-time transport optimization platform for Indian logistics.

## Architecture

### Layer 1: Real-time Tracking
- FastAPI backend with PostgreSQL database
- SQLAlchemy ORM with models for Companies, Trucks, Drivers, Routes, Bilties, and Trips
- RESTful CRUD APIs for managing transport documents and shipments

### Layer 2: ML-Based Prediction
- XGBoost delay prediction model trained on synthetic Indian route data
- Features: distance, weather, truck health, driver experience, historical delays
- Real-time inference endpoint: `POST /api/ml/predict`

### Layer 3: Risk Intelligence
- Cascade Risk Engine using NetworkX for dependency analysis
- Isolation Forest anomaly detection
- Truck Health Score calculator with rule-based deduction logic
- Risk level classification: Green (< 20%), Yellow (20-40%), Orange (40-60%), Red (> 60%)

### Layer 4: AI Copilot
- Google Gemini integration for conversational logistics assistance
- Simulation engine generating Continue/Reroute/Hold/SpeedUp options
- Decision support with risk-adjusted recommendations

## Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 13+
- Google Gemini API key (optional for mock mode)

### Installation

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup database**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your PostgreSQL credentials
   # DATABASE_URL=postgresql://user:password@localhost:5432/biltybook
   ```

4. **Initialize database**
   ```bash
   python -c "from database import init_db; init_db()"
   ```

5. **Load demo data**
   ```bash
   python -c "from main import app; from database import get_db; import requests; requests.post('http://localhost:8000/api/demo/init')"
   ```

## Running the Server

```bash
python main.py
```

Server starts at `http://localhost:8000`

### API Endpoints

#### Bilty Management
- `POST /api/bilty/create` - Create new bilty
- `GET /api/bilty/{id}` - Get bilty details
- `GET /api/bilty` - List all bilties
- `PUT /api/bilty/{id}` - Update bilty
- `DELETE /api/bilty/{id}` - Delete bilty

#### Trip Tracking  
- `POST /api/trips` - Create new trip
- `GET /api/trips` - List all trips
- `GET /api/trips/{id}` - Get trip details
- `PUT /api/trips/{id}` - Update trip status
- `POST /api/trips/{id}/complete` - Mark trip as completed

#### ML Predictions
- `POST /api/ml/predict` - Predict delay probability
- `POST /api/ml/health-score` - Calculate truck health score
- `POST /api/ml/cascade-analysis/{trip_id}` - Analyze cascade risks
- `POST /api/ml/anomaly-detection` - Detect anomalous trips

#### Decision Support
- `POST /api/copilot/chat` - AI logistics assistant
- `POST /api/simulation/{trip_id}` - Get action options

## Database Schema

### Key Models
- **Company**: Transport companies managing trucks and drivers
- **Truck**: Fleet vehicles with health scoring
- **Driver**: Licensed drivers with experience tracking
- **Route**: Predefined routes with distance/duration
- **Bilty**: Transport documents with sender/receiver details
- **Trip**: Active shipment with real-time tracking
- **CascadeRisk**: Dependency relationships and ripple effects
- **MLPrediction**: Historical predictions for model evaluation

## ML Pipeline

### Delay Prediction
**Input Features:**
- distance_km, avg_duration_hours
- truck_health_score (0-100)
- driver_experience_years
- weather_rain_mm
- highway_percentage
- weight_kg, capacity_tons
- historical_delay_hours
- time_of_day (0-23)
- is_monsoon (boolean)

**Output:**
- delay_probability (0-1)
- estimated_hours
- risk_level (green/yellow/orange/red)
- confidence score

### Truck Health Scoring
**Deduction Rules:**
- Age: -1 point per year over 10 years
- Mileage: -1 point per 100,000 km
- Service: -5 points per month overdue
- Accidents: -10 points per accident
- Maintenance: -20 to +5 based on score

**Rating:** Excellent (90+), Good (75-90), Fair (60-75), Poor (<60)

## Configuration

Edit `.env` file:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/biltybook
API_HOST=0.0.0.0
API_PORT=8000
GEMINI_API_KEY=your_api_key_here
```

## Testing

Initialize demo data:
```bash
curl -X POST http://localhost:8000/api/demo/init
```

Get active trips:
```bash
curl http://localhost:8000/api/trips
```

Predict delay:
```bash
curl -X POST http://localhost:8000/api/ml/predict \\
  -H "Content-Type: application/json" \\
  -d '{
    "distance_km": 500,
    "avg_duration_hours": 8,
    "truck_health_score": 85,
    "driver_experience_years": 10,
    "weather_rain_mm": 5,
    "highway_percentage": 80,
    "weight_kg": 10000,
    "capacity_tons": 20,
    "historical_delay_hours": 1.5,
    "time_of_day": 14,
    "is_monsoon": false
  }'
```

## Documentation

Access interactive API docs:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Performance Optimization

- Connection pooling with SQLAlchemy
- Async I/O support (ready for async/await)
- ML model caching with pickle serialization
- Graph algorithms optimized with NetworkX

## Future Enhancements

- WebSocket support for live updates
- Advanced route optimization with OR-Tools
- Multi-modal ML ensemble (Random Forest + XGBoost)
- Real-time GPS integration
- Mobile app with offline support
- Advanced reporting dashboard
