from typing import Dict, Any, List, Optional
from datetime import datetime

from app.core.adaptive_learning.difficulty_adjuster import DifficultyAdjuster
from app.core.adaptive_learning.pace_optimizer import PaceOptimizer
from app.core.adaptive_learning.format_transformer import ContentFormatTransformer

class AdaptationEngine:
    """
    The central orchestrator for adaptive learning logic.
    Ties together difficulty, pace, and format adaptation.
    """
    def __init__(self):
        self.difficulty_adjuster = DifficultyAdjuster()
        self.pace_optimizer = PaceOptimizer()
        self.format_transformer = ContentFormatTransformer()
        
    def generate_adaptation_directive(self, 
                                    profile: Dict[str, Any], 
                                    current_session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive adaptation directive for the learner.
        """
        # 1. Calculate Difficulty Adjustment
        difficulty_info = self.difficulty_adjuster.adjust_for_session(current_session_data, profile)
        
        # 2. Optimize Pacing
        engagement_score = current_session_data.get('recent_engagement_score', 0.5)
        pacing_info = self.pace_optimizer.optimize_session(profile, engagement_score)
        
        # 3. Content Format Recommendations
        learning_style = profile.get('learning_style', {})
        recommended_formats = self.format_transformer.recommend_formats(learning_style)
        primary_style = learning_style.get('primary', 'visual')
        format_directive = self.format_transformer.get_transformation_directive(primary_style)
        
        # 4. Consolidate into Directive
        directive = {
            "timestamp": datetime.utcnow().isoformat(),
            "difficulty": {
                "score": difficulty_info['difficulty_score'],
                "label": difficulty_info['label'],
                "action": "increase" if difficulty_info['changed'] and difficulty_info['difficulty_score'] > current_session_data.get('current_difficulty', 0.5) else "maintain"
            },
            "pacing": {
                "session_limit": pacing_info['optimal_session_duration'],
                "status": pacing_info['current_status'],
                "strategy": self.pace_optimizer.suggest_pacing_strategy(profile)
            },
            "content": {
                "primary_style": primary_style,
                "recommended_formats": [f['format'] for f in recommended_formats],
                "directive": format_directive
            },
            "summary": self._generate_summary(difficulty_info, pacing_info, primary_style)
        }
        
        return directive

    def _generate_summary(self, difficulty: Dict[str, Any], pacing: Dict[str, Any], style: str) -> str:
        """Create a human-readable summary of the adaptation"""
        summary = f"Adapting content for {style} style at {difficulty['label']} level. "
        if pacing['current_status'] == 'suggest_break':
            summary += "User engagement is dipping; suggesting a short break soon."
        else:
            summary += f"Optimal session duration estimated at {pacing['optimal_session_duration']} minutes."
        return summary
