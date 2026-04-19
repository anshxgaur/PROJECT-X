import os
from dotenv import load_dotenv

load_dotenv()

# Database (Use SQLite for development, PostgreSQL for production)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./biltybook.db")

# API Settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# ML Model
MODEL_PATH = os.getenv("MODEL_PATH", "./models/delay_predictor.pkl")

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Risk Thresholds
RISK_THRESHOLDS = {
    "green": 0.2,
    "yellow": 0.4,
    "orange": 0.6,
    "red": 0.8
}

# Truck Health Thresholds
HEALTH_THRESHOLDS = {
    "excellent": 90,
    "good": 75,
    "fair": 60,
    "poor": 0
}
