# Obsidian Vault - BiltyBook Intelligence

This is the Obsidian vault for managing billing data that integrates with the ML pipeline for advanced delay prediction.

## Structure

```
obsidian_vault/
├── Bilties/          # Billing documents with delivery data
│   ├── BLT-2024-001.md
│   ├── BLT-2024-002.md
│   └── BLT-2024-003.md
├── Analytics/        # Analysis and insights
└── Routes/           # Route information and optimization
```

## How to Use

### 1. Creating a New Bilty

Create a new markdown file in `Bilties/` folder with the naming convention: `BLT-YYYY-###.md`

**Example: BLT-2024-001.md**

```yaml
---
bilty_id: 1
bilty_number: BLT-2024-001
status: completed
date_created: 2024-01-15
sender_name: Company Name
receiver_name: Receiver Name
origin_city: Mumbai
destination_city: Delhi
distance_km: 1400
weight_kg: 5000
goods_type: Textiles
goods_value: ₹500000
rate_per_km: 15
total_amount: ₹21000
payment_status: paid
priority: high
weather_conditions: clear
highway_percentage: 85
actual_delay_hours: 2.5
scheduled_duration_hours: 48
---

# BLT-2024-001 - Mumbai to Delhi

## Shipment Details
- **Sender**: Company Name
- **Weight**: 5 tons

...
```

### 2. Required Fields (YAML Frontmatter)

| Field | Type | Description |
|-------|------|-------------|
| bilty_id | Integer | Unique ID |
| bilty_number | String | Format: BLT-YYYY-### |
| status | String | completed, active, delayed, pending |
| sender_name | String | Shipper company |
| receiver_name | String | Receiver company |
| origin_city | String | Source city |
| destination_city | String | Destination city |
| distance_km | Float | Route distance |
| weight_kg | Float | Shipment weight |
| goods_type | String | Type of goods |
| goods_value | String | Monetary value |
| rate_per_km | Float | Billing rate |
| total_amount | String | Total billing (e.g., ₹21000) |
| payment_status | String | pending, partial, paid |
| priority | String | low, medium, high, critical |
| weather_conditions | String | clear, rain, monsoon, fog, snow |
| highway_percentage | Float | % of highway in route (0-100) |
| actual_delay_hours | Float | Actual delay incurred |
| scheduled_duration_hours | Float | Expected journey duration |

### 3. Priority Levels Impact on ML

- **critical** (4): Highest priority - May reduce delay tolerance
- **high** (3): Important shipment
- **medium** (2): Standard shipping
- **low** (1): Flexible delivery

### 4. API Endpoints

**Get all bilties from Obsidian:**
```
GET /api/ml/obsidian/bilties
```

**Get specific bilty:**
```
GET /api/ml/obsidian/bilty/{bilty_number}
```

**Predict with billing impact:**
```
POST /api/ml/predict-with-billing
```
Request:
```json
{
  "distance_km": 1400,
  "avg_duration_hours": 48,
  "truck_health_score": 85
}
```

**Get billing analytics:**
```
GET /api/ml/obsidian/analytics
```

## Sample Analytics Output

```json
{
  "status": "success",
  "total_bilties": 3,
  "total_revenue": 57700,
  "average_delay_hours": 3.67,
  "risk_distribution": {
    "completed": 1,
    "active": 1,
    "delayed": 1,
    "pending": 0
  },
  "priority_distribution": {
    "critical": 1,
    "high": 1,
    "medium": 0,
    "low": 0
  },
  "payment_distribution": {
    "paid": 2,
    "pending": 1,
    "partial": 0
  }
}
```

## ML Integration

### How Obsidian Data Improves Predictions

1. **Training Data**: Historical bilties train the XGBoost model with real delays
2. **Feature Engineering**: 
   - Billing amount impact
   - Priority level scoring
   - Goods weight impact factors
3. **Context Matching**: ML finds similar routes in history
4. **Payment Status**: Affects priority calculation

### Feature Mapping

| Obsidian Field | ML Feature | Impact |
|---|---|---|
| priority | priority_score | Lower priority = faster |
| weather_conditions | weather_rain_mm | Rain/monsoon = more delay |
| highway_percentage | highway_percentage | More highways = faster |
| weight_kg | goods_weight_impact | Heavier = slower |
| total_amount | billing_amount | High value = more attention |
| actual_delay_hours | target variable | Trains prediction model |

## Best Practices

1. **Update delays promptly** - Record actual delays for accurate training
2. **Use consistent city names** - For better route matching
3. **Monitor payment status** - Impacts prioritization in recommendations
4. **Regular backups** - Keep Obsidian vault backed up
5. **Clear naming** - Use BLT-YYYY-### format consistently

## Enabling Obsidian Integration

The system automatically integrates Obsidian data into the ML pipeline on startup:

1. Reads all markdown files from `./obsidian_vault/Bilties/`
2. Extracts YAML frontmatter and features
3. Combines with synthetic training data
4. Trains XGBoost model with real historical delays
5. Uses billing context for predictions

## Troubleshooting

**"Vault path does not exist"**
- Ensure `obsidian_vault/Bilties/` directory exists

**"No bilties found"**
- Create `.md` files with proper YAML frontmatter in Bilties folder

**Features not being used**
- Restart backend to retrain ML model after adding new bilties
- Check YAML syntax in bilty files

**Dates not parsing**
- Use ISO format: `2024-01-15`
