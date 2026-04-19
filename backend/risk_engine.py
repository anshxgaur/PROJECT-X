import networkx as nx
from sklearn.ensemble import IsolationForest
import numpy as np
from datetime import datetime
from typing import List, Dict

class CascadeRiskEngine:
    """Cascade Risk Analysis using NetworkX"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
    
    def build_dependency_graph(self, trips: List[Dict]):
        """Build dependency graph of active trips"""
        self.graph.clear()
        
        # Add nodes for each trip
        for trip in trips:
            self.graph.add_node(trip['id'], **trip)
        
        # Create edges based on route dependencies
        # Trips on same route have dependency relationships
        route_trips = {}
        for trip in trips:
            route = trip.get('route_id', 'unknown')
            if route not in route_trips:
                route_trips[route] = []
            route_trips[route].append(trip['id'])
        
        # Connect sequential trips on same route
        for route, trip_ids in route_trips.items():
            for i in range(len(trip_ids) - 1):
                self.graph.add_edge(trip_ids[i], trip_ids[i+1], weight=0.8)
    
    def calculate_cascade_risk(self, primary_trip_id: int, primary_risk: float):
        """Calculate ripple risks for downstream trips"""
        cascade_risks = []
        
        try:
            # Get successor nodes (downstream trips)
            successors = list(nx.descendants(self.graph, primary_trip_id))
            
            for successor_id in successors:
                # Risk propagates with decay
                path_length = nx.shortest_path_length(self.graph, primary_trip_id, successor_id)
                decay_factor = 0.7 ** (path_length - 1)
                cascaded_risk = primary_risk * decay_factor
                
                cascade_risks.append({
                    'trip_id': primary_trip_id,
                    'affected_trip_id': successor_id,
                    'risk_score': cascaded_risk,
                    'impact_description': f"Downstream delay due to upstream trip {primary_trip_id}"
                })
        except nx.NetworkXNoPath:
            pass
        
        return cascade_risks
    
    def get_network_impact(self, primary_trip_id: int, primary_risk: float):
        """Get total network impact"""
        cascade_risks = self.calculate_cascade_risk(primary_trip_id, primary_risk)
        
        total_impact = primary_risk
        affected_trips = set([primary_trip_id])
        
        for risk in cascade_risks:
            total_impact += risk['risk_score']
            affected_trips.add(risk['affected_trip_id'])
        
        return {
            'primary_risk': primary_risk,
            'cascade_risks': cascade_risks,
            'total_network_impact': total_impact,
            'affected_trips': len(affected_trips)
        }


class AnomalyDetector:
    """Anomaly Detection using Isolation Forest"""
    
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.is_trained = False
    
    def train(self, trip_features: np.ndarray):
        """Train anomaly detector"""
        if len(trip_features) > 10:
            self.model.fit(trip_features)
            self.is_trained = True
    
    def detect_anomalies(self, trip_features: np.ndarray):
        """Detect anomalous trips"""
        if not self.is_trained or len(trip_features) == 0:
            return np.zeros(len(trip_features))
        
        # Returns -1 for anomalies, 1 for normal
        predictions = self.model.predict(trip_features)
        
        # Get anomaly scores (negative = more anomalous)
        scores = self.model.score_samples(trip_features)
        
        # Normalize scores to 0-1 (0 = normal, 1 = anomaly)
        anomaly_scores = 1 - (scores - scores.min()) / (scores.max() - scores.min() + 1e-6)
        
        return anomaly_scores


class TruckHealthRiskScorer:
    """Rule-based truck health scoring"""
    
    @staticmethod
    def calculate_health_score(truck_data: Dict) -> float:
        """
        Calculate truck health score (0-100)
        
        Deduction rules:
        - Age: -1 point per year over 10 years
        - Mileage: -1 point per 100,000 km
        - Service: -5 points per month overdue
        - Accidents: -10 points per accident
        - Maintenance score: Directly impacts (-20 to +5)
        """
        score = 100.0
        
        # Age penalty
        age_years = truck_data.get('age_years', 0)
        if age_years > 10:
            score -= (age_years - 10) * 1
        
        # Mileage penalty
        mileage = truck_data.get('mileage_km', 0)
        score -= (mileage / 100000) * 0.5
        
        # Service penalty
        days_since_service = truck_data.get('days_since_service', 0)
        months_overdue = max(0, (days_since_service - 180) / 30)
        score -= months_overdue * 5
        
        # Accident history penalty
        accidents = truck_data.get('accident_history', 0)
        score -= accidents * 10
        
        # Maintenance score adjustment
        maintenance_score = truck_data.get('maintenance_score', 0)
        score += (maintenance_score - 50) / 10
        
        # Clamp to 0-100
        return max(0, min(100, score))
    
    @staticmethod
    def get_health_rating(health_score: float) -> str:
        """Get health rating from score"""
        if health_score >= 90:
            return "excellent"
        elif health_score >= 75:
            return "good"
        elif health_score >= 60:
            return "fair"
        else:
            return "poor"
    
    @staticmethod
    def get_risk_factors(truck_data: Dict) -> List[str]:
        """Identify risk factors"""
        factors = []
        
        if truck_data.get('age_years', 0) > 15:
            factors.append("High age (>15 years)")
        
        if truck_data.get('mileage_km', 0) > 500000:
            factors.append("High mileage (>500k km)")
        
        if truck_data.get('days_since_service', 0) > 180:
            factors.append("Service overdue")
        
        if truck_data.get('accident_history', 0) > 2:
            factors.append("Multiple accident history")
        
        if truck_data.get('maintenance_score', 0) < 40:
            factors.append("Poor maintenance record")
        
        return factors
    
    @staticmethod
    def get_recommendations(truck_data: Dict) -> List[str]:
        """Get maintenance recommendations"""
        recommendations = []
        
        if truck_data.get('days_since_service', 0) > 150:
            recommendations.append("Schedule service immediately")
        
        if truck_data.get('mileage_km', 0) % 100000 < 10000:
            recommendations.append("Consider major overhaul soon")
        
        if truck_data.get('accident_history', 0) > 0:
            recommendations.append("Driver retraining recommended")
        
        if truck_data.get('age_years', 0) > 20:
            recommendations.append("Consider truck replacement")
        
        if not recommendations:
            recommendations.append("Continue regular maintenance")
        
        return recommendations


# Global instances
cascade_engine = CascadeRiskEngine()
anomaly_detector = AnomalyDetector()
health_scorer = TruckHealthRiskScorer()
