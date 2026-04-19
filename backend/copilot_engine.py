import google.generativeai as genai
from config import GEMINI_API_KEY
import json

COPILOT_SYSTEM_PROMPT = """You are an AI logistics assistant for BiltyBook Intelligence, a real-time truck transportation 
monitoring system in India. Your role is to provide actionable recommendations to fleet operators when transportation risks are detected.

You understand:
- Indian highway conditions and seasonal weather challenges (monsoon, etc.)
- Truck maintenance and health concerns
- Driver behavior and safety protocols
- Route optimization and delay prevention
- Risk mitigation strategies

When given a trip situation with identified risks, provide:
1. Clear analysis of the current situation
2. Specific, actionable recommendations (max 3-4 actions)
3. Risk assessment and potential impact
4. Alternative approaches if applicable

Be concise, professional, and prioritize safety and timeline adherence."""

class CopilotEngine:
    """Gemini-based AI Copilot for logistics decisions"""
    
    def __init__(self, api_key: str = GEMINI_API_KEY):
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    def query_copilot(self, trip_context: dict, risk_level: str, message: str) -> dict:
        """Query Copilot for logistics advice"""
        
        if not self.model:
            # Return mock response if no API key
            return self._mock_response(trip_context, risk_level, message)
        
        try:
            # Build context message
            context_text = f"""
Trip Context:
- Trip ID: {trip_context.get('trip_id')}
- Route: {trip_context.get('origin')} → {trip_context.get('destination')}
- Distance: {trip_context.get('distance_km')} km
- Truck: {trip_context.get('truck_model')}, Health: {trip_context.get('truck_health')}%
- Driver: {trip_context.get('driver_experience')} years experience
- Current Risk Level: {risk_level}
- Delay Probability: {trip_context.get('delay_probability')*100:.1f}%
- Expected Delay: {trip_context.get('estimated_delay_hours')} hours

Issue: {message}

Provide actionable recommendations to address this situation.
"""
            
            response = self.model.generate_content(
                COPILOT_SYSTEM_PROMPT + "\n\n" + context_text
            )
            
            advice_text = response.text
            
            # Parse advice into structured format
            return {
                'advice': advice_text,
                'actions': self._extract_actions(advice_text),
                'priority': self._assess_priority(risk_level),
                'model': 'gemini-pro'
            }
        
        except Exception as e:
            print(f"Copilot error: {e}")
            return self._mock_response(trip_context, risk_level, message)
    
    def _mock_response(self, trip_context: dict, risk_level: str, message: str) -> dict:
        """Generate mock response for testing"""
        
        advice_map = {
            'red': f"URGENT: Trip {trip_context.get('trip_id')} is at critical risk. {message}. "
                   "Recommend immediate contact with driver, assess truck condition, and consider rerouting.",
            'orange': f"HIGH RISK: Trip {trip_context.get('trip_id')} showing warning signs. {message}. "
                     "Monitor closely and prepare contingency plans.",
            'yellow': f"MODERATE RISK: Trip {trip_context.get('trip_id')} needs attention. {message}. "
                     "Proactive monitoring will help prevent escalation.",
            'green': f"Normal operations for Trip {trip_context.get('trip_id')}. {message}"
        }
        
        actions_map = {
            'red': [
                "Contact driver immediately for status check",
                "Dispatch support vehicle or arrange for truck pickup",
                "Notify receiver of potential delay",
                "Review alternative routes"
            ],
            'orange': [
                "Monitor real-time GPS updates",
                "Check weather conditions ahead",
                "Prepare communication with receiver",
                "Have backup driver on standby"
            ],
            'yellow': [
                "Monitor trip progress",
                "Keep driver informed of deadline",
                "Plan rest stops efficiently"
            ],
            'green': [
                "Continue normal monitoring",
                "Plan next delivery assignment"
            ]
        }
        
        priority_map = {
            'red': 'immediate',
            'orange': 'urgent',
            'yellow': 'normal',
            'green': 'low'
        }
        
        return {
            'advice': advice_map.get(risk_level, advice_map['green']),
            'actions': actions_map.get(risk_level, actions_map['green']),
            'priority': priority_map.get(risk_level, 'normal'),
            'model': 'mock'
        }
    
    def _extract_actions(self, text: str) -> list:
        """Extract actionable items from advice"""
        actions = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith(('•', '-', '*', '1.', '2.', '3.', '4.')) and len(line) > 5:
                action = line.lstrip('•-*123456789. ').strip()
                if action and len(action) > 5:
                    actions.append(action)
        
        return actions[:4]  # Limit to 4 actions
    
    def _assess_priority(self, risk_level: str) -> str:
        """Assess action priority"""
        priority_map = {
            'red': 'immediate',
            'orange': 'urgent',
            'yellow': 'normal',
            'green': 'low'
        }
        return priority_map.get(risk_level, 'normal')


def generate_simulation_cards(trip_data: dict, current_risk: float) -> list:
    """Generate simulation cards with action options"""
    
    options = []
    
    # Option 1: Continue
    options.append({
        'action': 'continue',
        'description': 'Continue on current route with current speed',
        'estimated_impact': current_risk * 1.05,  # Slight increase
        'risk_reduction': 0.0
    })
    
    # Option 2: Reroute
    if current_risk > 0.4:
        options.append({
            'action': 'reroute',
            'description': 'Take alternative route to avoid delays',
            'estimated_impact': current_risk * 0.6,
            'risk_reduction': current_risk * 0.4
        })
    
    # Option 3: Hold
    if current_risk > 0.5:
        options.append({
            'action': 'hold',
            'description': 'Wait for conditions to improve',
            'estimated_impact': current_risk * 0.7,
            'risk_reduction': current_risk * 0.3
        })
    
    # Option 4: Speed up
    if current_risk > 0.3 and trip_data.get('truck_health', 100) > 70:
        options.append({
            'action': 'speedup',
            'description': 'Increase speed (safely) to meet deadline',
            'estimated_impact': current_risk * 1.2,
            'risk_reduction': -0.2
        })
    
    return options


# Global instance
copilot_engine = CopilotEngine()
