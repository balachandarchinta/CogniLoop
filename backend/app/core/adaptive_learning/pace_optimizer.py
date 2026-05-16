from typing import Dict, Any, List

class PaceOptimizer:
    """
    Optimizes learning pace, session duration, and break frequency.
    """
    def __init__(self):
        self.min_session_duration = 10  # minutes
        self.max_session_duration = 90  # minutes
        
    def optimize_session(self, profile: Dict[str, Any], current_engagement: float) -> Dict[str, Any]:
        """
        Determine if the user needs a break or if the session should be extended/shortened.
        """
        characteristics = profile.get('cognitive_characteristics', {})
        base_attention_span = characteristics.get('attention_span_minutes', 25)
        
        # Calculate optimal duration based on attention span and current engagement
        # If engagement is high, we can stretch the session
        optimal_duration = base_attention_span * (0.5 + current_engagement)
        optimal_duration = max(self.min_session_duration, min(optimal_duration, self.max_session_duration))
        
        # Determine break frequency
        # Low attention span users need more frequent breaks
        if base_attention_span < 20:
            break_frequency = 15 # every 15 mins
        elif base_attention_span < 40:
            break_frequency = 25
        else:
            break_frequency = 45
            
        return {
            "optimal_session_duration": round(optimal_duration, 1),
            "break_frequency_minutes": break_frequency,
            "current_status": "continue" if current_engagement > 0.4 else "suggest_break"
        }

    def suggest_pacing_strategy(self, profile: Dict[str, Any]) -> str:
        """Categorical pacing strategy based on profile"""
        characteristics = profile.get('cognitive_characteristics', {})
        speed = characteristics.get('comprehension_speed', 'moderate')
        
        if speed == 'fast':
            return "Accelerated: High-density content with rapid progression."
        elif speed == 'slow':
            return "Steady: Modular content with frequent reinforcement loops."
        else:
            return "Standard: Balanced progression with periodic reviews."
