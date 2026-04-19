import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pickle
import os
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
import json
from pathlib import Path


class DelayPredictorPipeline:
    """XGBoost-based delay prediction model with Obsidian billing integration"""
    
    def __init__(self, model_path="models/delay_predictor.pkl", vault_path=None):
        self.model_path = model_path
        self.vault_path = vault_path or os.path.join(os.path.dirname(__file__), '..', 'obsidian_vault')
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'distance_km', 'avg_duration_hours', 'truck_health_score',
            'driver_experience_years', 'weather_rain_mm', 'highway_percentage',
            'weight_kg', 'capacity_tons', 'historical_delay_hours',
            'time_of_day', 'is_monsoon', 'billing_amount', 'priority_score', 'goods_weight_impact'
        ]
        self.load_or_create_model()
    
    def load_obsidian_bilties(self):
        """Load billing data from Obsidian vault"""
        try:
            from obsidian_reader import ObsidianReader
            reader = ObsidianReader(self.vault_path)
            return reader.get_all_bilties()
        except Exception as e:
            print(f"Warning: Could not load Obsidian bilties: {e}")
            return []
    
    def load_or_create_model(self):
        """Load existing model or create new one"""
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
                self.model = model_data['model']
                self.scaler = model_data['scaler']
        else:
            # Create and train on synthetic + Obsidian data
            self.train_on_synthetic_data()
    
    def generate_synthetic_data(self, n_samples=2000):
        """Generate synthetic trip data for training"""
        np.random.seed(42)
        
        data = {
            'distance_km': np.random.uniform(50, 1000, n_samples),
            'avg_duration_hours': np.random.uniform(2, 48, n_samples),
            'truck_health_score': np.random.uniform(60, 100, n_samples),
            'driver_experience_years': np.random.uniform(1, 30, n_samples),
            'weather_rain_mm': np.random.exponential(10, n_samples),
            'highway_percentage': np.random.uniform(0, 100, n_samples),
            'weight_kg': np.random.uniform(1000, 20000, n_samples),
            'capacity_tons': np.random.uniform(5, 30, n_samples),
            'historical_delay_hours': np.random.exponential(2, n_samples),
            'time_of_day': np.random.randint(0, 24, n_samples),
            'is_monsoon': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
            'billing_amount': np.random.uniform(5000, 50000, n_samples),
            'priority_score': np.random.choice([1, 2, 3, 4], n_samples, p=[0.4, 0.3, 0.2, 0.1]),
            'goods_weight_impact': np.random.uniform(0.5, 2.0, n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Create synthetic delays based on features
        df['delay_hours'] = (
            0.05 * df['distance_km'] +
            2 * df['weather_rain_mm'] / 10 +
            0.5 * (100 - df['truck_health_score']) / 10 +
            0.3 * (30 - df['driver_experience_years']) / 10 +
            1.5 * df['is_monsoon'] +
            0.02 * df['weight_kg'] / 1000 +
            -0.5 * df['priority_score'] / 4 +
            0.3 * df['goods_weight_impact'] +
            np.random.normal(0, 2, n_samples)
        )
        
        df['delay_hours'] = np.maximum(df['delay_hours'], 0)
        
        return df
    
    def obsidian_to_ml_features(self, bilty: dict) -> dict:
        """Convert Obsidian bilty data to ML features"""
        priority_map = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
        weather_map = {'clear': 0, 'rain': 5, 'monsoon': 20, 'fog': 3, 'snow': 15}
        
        return {
            'distance_km': bilty['distance_km'],
            'avg_duration_hours': bilty['scheduled_duration_hours'],
            'truck_health_score': 80,
            'driver_experience_years': 10,
            'weather_rain_mm': weather_map.get(bilty['weather_conditions'], 0),
            'highway_percentage': bilty['highway_percentage'],
            'weight_kg': bilty['weight_kg'],
            'capacity_tons': 15,
            'historical_delay_hours': bilty['actual_delay_hours'],
            'time_of_day': 12,
            'is_monsoon': 1 if 'monsoon' in bilty['weather_conditions'].lower() else 0,
            'billing_amount': bilty['total_amount'],
            'priority_score': priority_map.get(bilty['priority'].lower(), 2),
            'goods_weight_impact': bilty['weight_kg'] / 10000
        }
    
    def train_on_synthetic_data(self, n_samples=2000):
        """Train model on synthetic data + Obsidian historical data"""
        df = self.generate_synthetic_data(n_samples)
        
        # Load Obsidian bilties and add to training data
        obsidian_bilties = self.load_obsidian_bilties()
        if obsidian_bilties:
            obsidian_features = []
            obsidian_delays = []
            for bilty in obsidian_bilties:
                features = self.obsidian_to_ml_features(bilty)
                obsidian_features.append(features)
                obsidian_delays.append(bilty['actual_delay_hours'])
            
            if obsidian_features:
                df_obsidian = pd.DataFrame(obsidian_features)
                df_obsidian['delay_hours'] = obsidian_delays
                df = pd.concat([df_obsidian, df], ignore_index=True)
        
        X = df[self.feature_names]
        y = df['delay_hours']
        
        X_scaled = self.scaler.fit_transform(X)
        
        self.model = XGBRegressor(
            max_depth=6,
            learning_rate=0.1,
            n_estimators=100,
            random_state=42,
            objective='reg:squarederror'
        )
        self.model.fit(X_scaled, y)
        
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump({'model': self.model, 'scaler': self.scaler}, f)
    
    def predict(self, features_dict):
        """Make delay prediction with billing considerations"""
        features_array = np.array([[
            features_dict['distance_km'],
            features_dict['avg_duration_hours'],
            features_dict['truck_health_score'],
            features_dict['driver_experience_years'],
            features_dict['weather_rain_mm'],
            features_dict['highway_percentage'],
            features_dict['weight_kg'],
            features_dict['capacity_tons'],
            features_dict['historical_delay_hours'],
            features_dict['time_of_day'],
            features_dict['is_monsoon'],
            features_dict.get('billing_amount', 10000),
            features_dict.get('priority_score', 2),
            features_dict.get('goods_weight_impact', 1.0)
        ]])
        
        features_scaled = self.scaler.transform(features_array)
        
        estimated_hours = self.model.predict(features_scaled)[0]
        estimated_hours = max(0, estimated_hours)
        
        base_hours = features_dict['avg_duration_hours']
        delay_probability = min(1.0, estimated_hours / (base_hours + 1))
        
        if delay_probability < 0.2:
            risk_level = "green"
        elif delay_probability < 0.4:
            risk_level = "yellow"
        elif delay_probability < 0.6:
            risk_level = "orange"
        else:
            risk_level = "red"
        
        billing_impact = "low"
        if features_dict.get('billing_amount', 0) > 20000:
            billing_impact = "high"
        elif features_dict.get('billing_amount', 0) > 10000:
            billing_impact = "medium"
        
        return {
            'delay_probability': float(delay_probability),
            'estimated_hours': float(estimated_hours),
            'risk_level': risk_level,
            'confidence': 0.85,
            'billing_impact': billing_impact,
            'billing_amount': features_dict.get('billing_amount', 0),
            'priority_level': features_dict.get('priority_score', 2)
        }


# Global instance
delay_predictor = DelayPredictorPipeline()
