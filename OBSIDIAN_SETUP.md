# Obsidian + ML Integration Setup Guide

## 🎯 What This Does

Your ML pipeline now reads **billing data from Obsidian** and uses it to:
- Train delay prediction models with real historical data
- Include billing impact in risk calculations
- Match new trips with similar historical routes
- Analyze profitability vs. risk tradeoffs

## 📁 Project Structure

```
GEN SOL/
├── backend/
│   ├── obsidian_reader.py       (NEW) Reads Obsidian markdown files
│   ├── ml_pipeline.py            (UPDATED) Integrates billing data
│   └── routers/
│       └── ml.py                 (UPDATED) New Obsidian endpoints
├── obsidian_vault/               (NEW) Billing data storage
│   ├── Bilties/
│   │   ├── BLT-2024-001.md
│   │   ├── BLT-2024-002.md
│   │   ├── BLT-2024-003.md
│   │   └── _TEMPLATE.md
│   ├── Analytics/
│   ├── Routes/
│   └── README.md
```

## 🚀 Getting Started

### Step 1: Enable Obsidian Readings

The system automatically loads Obsidian data. No configuration needed!

### Step 2: Add Your First Bilty

1. Open `obsidian_vault/Bilties/` folder
2. Copy `_TEMPLATE.md` and name it `BLT-2024-001.md`
3. Fill in the YAML frontmatter
4. Restart backend to retrain model

### Step 3: Test Integration

```bash
# Get all bilties from Obsidian
curl http://localhost:8000/api/ml/obsidian/bilties

# Get billing analytics
curl http://localhost:8000/api/ml/obsidian/analytics

# Make prediction with billing impact
curl -X POST http://localhost:8000/api/ml/predict-with-billing \
  -H "Content-Type: application/json" \
  -d '{
    "distance_km": 1400,
    "avg_duration_hours": 48,
    "truck_health_score": 85,
    "driver_experience_years": 10,
    "weather_rain_mm": 0,
    "highway_percentage": 85,
    "weight_kg": 5000,
    "capacity_tons": 15,
    "historical_delay_hours": 2,
    "time_of_day": 12,
    "is_monsoon": 0
  }'
```

## 📊 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/ml/obsidian/bilties` | GET | List all bilties from Obsidian |
| `/api/ml/obsidian/bilty/{number}` | GET | Get specific bilty |
| `/api/ml/obsidian/analytics` | GET | Analytics dashboard |
| `/api/ml/predict-with-billing` | POST | Predict with billing context |

## 🧠 How ML Uses Obsidian Data

### Training Phase
```
1. Load Obsidian bilties
2. Extract features:
   - distance_km, weight_kg, hardware%, priority
   - billing_amount, goods_weight_impact
   - weather, highway%, scheduled time
3. Target: actual_delay_hours
4. Train XGBoost ✓
```

### Prediction Phase
```
1. Receive trip features
2. Load similar historical routes from Obsidian
3. Predict delay with ML model
4. Add billing impact score
5. Return: delay_probability, risk_level, billing_impact
```

## 💡 Key Features

### 1. Priority-Based Predictions
- **Critical**: 4x weighting - needs fastest delivery
- **High**: 3x weighting
- **Medium**: 2x weighting (default)
- **Low**: 1x weighting - flexible

### 2. Billing Impact Analysis
```
billing_amount < ₹10k → "low impact"
₹10k - ₹20k → "medium impact"
> ₹20k → "high impact"
```

### 3. Historical Route Matching
```
For each prediction:
- Find similar routes in Obsidian history
- Show actual delays from similar trips
- Use in confidence scoring
```

### 4. Performance Tracking
```
Analytics dashboard shows:
- Total revenue from bilties
- Average delays by route
- Payment status distribution
- Risk distribution
```

## 📝 Bilty File Format

### Required Fields
```yaml
bilty_number: BLT-2024-001          # Unique identifier
distance_km: 1400                    # Route distance
weight_kg: 5000                      # Shipment weight
total_amount: ₹21000                 # Billing amount
priority: high                       # low/medium/high/critical
weather_conditions: clear            # clear/rain/monsoon
highway_percentage: 85               # 0-100
actual_delay_hours: 2.5              # Historical delay
scheduled_duration_hours: 48         # Expected time
```

### Optional Fields
```yaml
status: completed                    # pending/active/delayed/completed
payment_status: paid                 # pending/partial/paid
sender_name: Company A               # Shipper
receiver_name: Company B             # Receiver
```

## 🔧 Customization

### Change Model Features
Edit `ml_pipeline.py`:
```python
feature_names = [
    'distance_km', 'weight_kg', 'billing_amount',
    'priority_score', 'weather_score', ...
]
```

### Change Thresholds
Edit `ml_pipeline.py` risk calculation:
```python
if delay_probability < 0.2:
    risk_level = "green"
elif delay_probability < 0.4:
    risk_level = "yellow"
```

### Add New Analytics
Edit `routers/ml.py` `/obsidian/analytics` endpoint:
```python
# Add your custom metrics
goods_distribution = {
    'electronics': 0,
    'food': 0,
    'textiles': 0
}
```

## 🎓 Example Workflow

### 1. You complete a trip
```
Trip: Mumbai → Delhi, 1400km, 5 tons textiles
Actual delay: 2.5 hours
Billing: ₹21,000 paid
Priority: High
```

### 2. Create Obsidian bilty
```markdown
---
bilty_number: BLT-2024-001
distance_km: 1400
weight_kg: 5000
actual_delay_hours: 2.5
total_amount: ₹21000
priority: high
---
```

### 3. Next similar trip
```json
Request: Same route, similar conditions
ML Response: {
  "delay_probability": 0.18,
  "estimated_hours": 2.5,
  "risk_level": "green",
  "matching_historical_bilty": "BLT-2024-001"
}
```

### 4. Action
```
Risk is LOW based on historical data ✓
Expected: 2.5 hours delay
Confidence: 85%
```

## ⚙️ Behind the Scenes

### obsidian_reader.py
- Parses YAML frontmatter from markdown
- Extracts features for ML
- Provides training data
- Enables analytics

### ml_pipeline.py (Updated)
- Loads Obsidian bilties on startup
- Includes billing features in model
- Trains on historical + synthetic data
- Returns billing impact in predictions

### routers/ml.py (Updated)
- `/obsidian/bilties` - Get all data
- `/obsidian/analytics` - Dashboard metrics
- `/predict-with-billing` - Smart predictions
- `/obsidian/bilty/{id}` - Specific bilty

## 🚨 Troubleshooting

**Model not using Obsidian data?**
- Restart backend: `python main.py`
- Check bilties exist in `obsidian_vault/Bilties/`
- Verify YAML syntax

**Analytics showing zero?**
- Create at least 1 bilty with complete data
- Run the analytics endpoint

**Predictions still generic?**
- Add more historical bilties (10+ for better training)
- Ensure actual_delay_hours is realistic

## 📚 Next Steps

1. **Add historical data** - Import past trips to Obsidian
2. **Monitor analytics** - Track patterns over time
3. **Refine priorities** - Adjust based on business needs
4. **Scale predictions** - Build recommendation engine on top

---

**Questions?** Check `obsidian_vault/README.md` for detailed docs!
