# 🚀 Obsidian + ML Quick Start

## What Changed?

Your ML model now reads **billing data from Obsidian markdown files** and uses it to predict delays more accurately!

## In This Folder

```
📁 obsidian_vault/
├── 📂 Bilties/                  ← Add billing data here
│   ├── BLT-2024-001.md         (Sample: Electronics)
│   ├── BLT-2024-002.md         (Sample: Textiles)
│   ├── BLT-2024-003.md         (Sample: Agriculture)
│   └── _TEMPLATE.md             (Copy this to add new bilty)
├── 📂 Analytics/                (Monthly insights)
├── 📂 Routes/                   (Route optimization)
└── README.md                    (Detailed docs)
```

## How to Use

### 1️⃣ **Add Your First Bilty**

Copy template, fill in data:
```bash
1. Open: obsidian_vault/Bilties/_TEMPLATE.md
2. Copy to: BLT-2024-004.md
3. Fill in the YAML frontmatter
4. Save
```

Required fields:
```yaml
bilty_number: BLT-2024-004
distance_km: 1200
weight_kg: 3000
total_amount: ₹18000
priority: high
actual_delay_hours: 1.5
```

### 2️⃣ **Restart Backend**

```bash
cd backend
python main.py
```

✨ Model retrains with your new data!

### 3️⃣ **Test Integration**

```bash
# Get all bilties
curl http://localhost:8000/api/ml/obsidian/bilties

# Get analytics
curl http://localhost:8000/api/ml/obsidian/analytics

# Make smart prediction
curl -X POST http://localhost:8000/api/ml/predict-with-billing \
  -H "Content-Type: application/json" \
  -d '{
    "distance_km": 1200,
    "avg_duration_hours": 36,
    "truck_health_score": 85,
    "driver_experience_years": 10,
    "weather_rain_mm": 0,
    "highway_percentage": 80,
    "weight_kg": 3000,
    "capacity_tons": 15,
    "historical_delay_hours": 1,
    "time_of_day": 10,
    "is_monsoon": 0
  }'
```

## What's New

### New API Endpoints

```
GET  /api/ml/obsidian/bilties              → Get all billing data
GET  /api/ml/obsidian/bilty/{number}       → Get specific bilty
GET  /api/ml/obsidian/analytics            → Dashboard metrics
POST /api/ml/predict-with-billing          → Smart prediction
```

### New ML Features

- 🏦 **Billing Amount** - High-value shipments handled differently
- ⭐ **Priority Level** - Critical orders = less delay
- 📦 **Goods Weight** - Heavier goods = planning adjusted
- 📍 **Historical Matching** - Shows similar past trips
- 📈 **Financial Impact** - Tracks revenue vs. risk

## Example

### Your Bilty
```yaml
---
bilty_number: BLT-2024-004
distance_km: 1200
weight_kg: 3000
total_amount: ₹18000
priority: high
weather_conditions: clear
highway_percentage: 80
actual_delay_hours: 1.5
scheduled_duration_hours: 36
---
```

### ML Output
```json
{
  "delay_probability": 0.12,
  "estimated_hours": 1.5,
  "risk_level": "green",
  "billing_impact": "medium",
  "billing_amount": 18000,
  "priority_level": 3,
  "trained_on_obsidian_data": true
}
```

✅ ML **learned from your 4 past trips** now!

## Files to Read

1. **Quick Overview** ← You are here
2. **Full Setup**: `OBSIDIAN_SETUP.md`
3. **Vault Docs**: `obsidian_vault/README.md`
4. **Integration Details**: `OBSIDIAN_INTEGRATION_SUMMARY.md`

## Common Tasks

### Add a New Bilty
```
1. Open _TEMPLATE.md
2. Copy to BLT-2024-XXX.md
3. Fill YAML fields
4. Restart backend (python main.py)
```

### View Analytics
```bash
curl http://localhost:8000/api/ml/obsidian/analytics
```

### Get Specific Bilty
```bash
curl "http://localhost:8000/api/ml/obsidian/bilty/BLT-2024-001"
```

### Predict Like Pro
```bash
curl -X POST http://localhost:8000/api/ml/predict-with-billing \
  -H "Content-Type: application/json" \
  -d '{ ...features... }'
```

## Key Insight 💡

Before: ML = Synthetic data only  
After: ML = Real history + Synthetic data

**More data = Better predictions!**

---

**Ready? Create your first Obsidian bilty now! 🎉**
