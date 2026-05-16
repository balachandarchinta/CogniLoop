from datetime import datetime
from typing import Dict, Any

from app.core.cognitive_profiling.learning_style_classifier import LearningStyleClassifier
from app.core.cognitive_profiling.attention_analyzer import AttentionSpanAnalyzer
from app.core.cognitive_profiling.comprehension_speed import ComprehensionSpeedAssessor
from app.core.cognitive_profiling.retention_analyzer import RetentionAnalyzer


class ProfileEvolutionManager:
    """Manages the evolution and updating of a learner's cognitive profile."""
    def __init__(self):
        self.update_threshold = 50  # New data points before update
        self.confidence_decay_rate = 0.95
        
        self.classifier = LearningStyleClassifier()
        self.attention_analyzer = AttentionSpanAnalyzer()
        self.speed_assessor = ComprehensionSpeedAssessor()
        self.retention_analyzer = RetentionAnalyzer()
        
    def should_update_profile(self, profile: Any, new_data_points: int) -> bool:
        """Determine if profile should be updated"""
        if new_data_points >= self.update_threshold:
            return True
            
        confidence_metrics = getattr(profile, 'confidence_metrics', {})
        if confidence_metrics.get('overall_confidence', 1.0) < 0.6:
            return True
            
        # Simplified change detection
        return False

    def merge_learning_styles(self, current: Dict[str, Any], new_style: Dict[str, Any], weight_new: float = 0.3) -> Dict[str, Any]:
        """Merge learning style predictions."""
        merged = current.copy()
        for style, score in new_style.get('scores', {}).items():
            curr_score = current.get('scores', {}).get(style, 0.25)
            merged.setdefault('scores', {})[style] = (curr_score * (1 - weight_new)) + (score * weight_new)
            
        # Re-determine primary/secondary
        sorted_styles = sorted(merged.get('scores', {}).items(), key=lambda x: x[1], reverse=True)
        if sorted_styles:
            merged['primary'] = sorted_styles[0][0]
            if len(sorted_styles) > 1:
                merged['secondary'] = sorted_styles[1][0]
        return merged

    def update_characteristics(self, current_chars: Dict[str, Any], new_data: Any) -> Dict[str, Any]:
        """Update cognitive characteristics."""
        speed_assessment = self.speed_assessor.assess_speed(new_data)
        retention = self.retention_analyzer.calculate_retention_rate(new_data)
        
        updated = current_chars.copy()
        updated['comprehension_speed'] = speed_assessment['category']
        updated['retention_rate'] = retention['retention_rate']
        
        session_events = getattr(new_data, 'events', [])
        attention = self.attention_analyzer.analyze_session(session_events)
        updated['attention_span_minutes'] = attention['average_attention_span']
        
        return updated
        
    def update_patterns(self, current_patterns: Dict[str, Any], new_data: Any) -> Dict[str, Any]:
        """Update behavioral patterns."""
        # Stub logic
        return current_patterns

    def update_profile(self, current_profile: Any, new_data: Any) -> Dict[str, Any]:
        """Update cognitive profile with new data"""
        new_learning_style = self.classifier.predict(new_data)
        
        updated_profile = {
            'learning_style': self.merge_learning_styles(
                getattr(current_profile, 'learning_style', {}),
                new_learning_style,
                weight_new=0.3
            ),
            'cognitive_characteristics': self.update_characteristics(
                getattr(current_profile, 'cognitive_characteristics', {}),
                new_data
            ),
            'behavioral_patterns': self.update_patterns(
                getattr(current_profile, 'behavioral_patterns', {}),
                new_data
            ),
            'profile_version': getattr(current_profile, 'profile_version', 0) + 1,
            'updated_at': datetime.utcnow()
        }
        return updated_profile
