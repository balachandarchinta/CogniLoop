import numpy as np
from typing import Dict, Any, List, Optional

class DifficultyAdjuster:
    """
    Dynamically adjusts content difficulty based on learner performance 
    and cognitive profile.
    """
    def __init__(self):
        self.difficulty_levels = ["Beginner", "Intermediate", "Advanced"]
        self.learning_rate = 0.1
        
    def calculate_new_difficulty(self, 
                               current_difficulty: float, 
                               performance_score: float, 
                               cognitive_profile: Dict[str, Any]) -> float:
        """
        Calculate new difficulty score (0.0 to 1.0) using a simplified 
        adaptation logic.
        
        Logic:
        - If score > 0.8: Increase difficulty
        - If score < 0.5: Decrease difficulty
        - Factor in 'comprehension_speed' and 'retention_rate' from profile
        """
        target_score = 0.75  # The "Zone of Proximal Development" target
        
        error = performance_score - target_score
        
        # Base adjustment
        adjustment = error * self.learning_rate
        
        # Profile-based modifiers
        characteristics = cognitive_profile.get('cognitive_characteristics', {})
        speed = characteristics.get('comprehension_speed', 'moderate')
        retention = characteristics.get('retention_rate', 0.7)
        
        if speed == 'fast':
            adjustment *= 1.2
        elif speed == 'slow':
            adjustment *= 0.8
            
        # If retention is high, we can push difficulty faster
        if retention > 0.85:
            adjustment *= 1.1
            
        new_difficulty = current_difficulty + adjustment
        
        # Clip between 0.1 and 1.0
        return float(np.clip(new_difficulty, 0.1, 1.0))

    def get_difficulty_label(self, score: float) -> str:
        """Convert numerical score to categorical label"""
        if score < 0.4:
            return "Beginner"
        elif score < 0.75:
            return "Intermediate"
        else:
            return "Advanced"

    def adjust_for_session(self, current_session_data: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform a session-level difficulty adjustment.
        """
        scores = current_session_data.get('assessment_scores', [])
        if not scores:
            return {"difficulty_score": 0.5, "label": "Intermediate", "changed": False}
            
        avg_score = sum(scores) / len(scores)
        current_diff = current_session_data.get('current_difficulty', 0.5)
        
        new_diff = self.calculate_new_difficulty(current_diff, avg_score, profile)
        
        return {
            "difficulty_score": new_diff,
            "label": self.get_difficulty_label(new_diff),
            "changed": abs(new_diff - current_diff) > 0.05
        }
