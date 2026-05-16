import numpy as np
from scipy.optimize import curve_fit
import statistics
from typing import List, Dict, Any

class RetentionAnalyzer:
    """Analyzes memory retention based on Ebbinghaus Forgetting Curve."""
    def __init__(self):
        self.base_forgetting_rate = 0.5  # 50% forgotten after 1 day without review
        
    def calculate_retention_rate(self, learner_data: Any) -> Dict[str, Any]:
        """Calculate learner's retention rate"""
        retention_tests = []
        
        learned_concepts = getattr(learner_data, 'learned_concepts', [])
        
        for concept in learned_concepts:
            initial_score = getattr(concept, 'initial_assessment_score', 1.0)
            if initial_score == 0:
                continue
                
            reviews = getattr(concept, 'reviews', [])
            for review in reviews:
                time_elapsed = (review.date - concept.learned_date).days
                retention_score = review.score / initial_score
                
                retention_tests.append({
                    'time_elapsed': max(time_elapsed, 1), # Avoid division by zero issues
                    'retention_score': retention_score,
                    'concept_difficulty': getattr(concept, 'difficulty', 1.0)
                })
        
        # If no data, return defaults
        if not retention_tests:
            def default_forgetting(t, a=1.0, b=0.1):
                return a * np.exp(-b * t)
            
            return {
                'retention_rate': 0.8,
                'forgetting_curve': {
                    'function': default_forgetting,
                    'parameters': {'a': 1.0, 'b': 0.1},
                    'half_life': np.log(2) / 0.1
                },
                'optimal_review_intervals': [1, 3, 7, 14, 30]
            }
        
        # Fit personalized forgetting curve
        retention_curve = self.fit_forgetting_curve(retention_tests)
        
        # Calculate overall retention rate
        avg_retention = statistics.mean([t['retention_score'] for t in retention_tests])
        
        return {
            'retention_rate': avg_retention,
            'forgetting_curve': retention_curve,
            'optimal_review_intervals': self.calculate_review_intervals(retention_curve)
        }
        
    def fit_forgetting_curve(self, retention_tests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fit personalized forgetting curve"""
        
        def forgetting_function(t, a, b):
            """R(t) = a * e^(-b*t)"""
            return a * np.exp(-b * t)
            
        times = [t['time_elapsed'] for t in retention_tests]
        scores = [t['retention_score'] for t in retention_tests]
        
        try:
            # Fit curve
            params, _ = curve_fit(forgetting_function, times, scores, p0=[1.0, 0.1])
            a, b = params[0], params[1]
            
            # Ensure b is positive so half_life is valid
            if b <= 0:
                b = 0.001
        except Exception:
            # Fallback if fit fails
            a, b = 1.0, 0.1
            
        return {
            'function': forgetting_function,
            'parameters': {'a': a, 'b': b},
            'half_life': np.log(2) / b  # Time to forget 50%
        }
        
    def calculate_review_intervals(self, forgetting_curve: Dict[str, Any]) -> List[int]:
        """Calculate optimal review intervals using spaced repetition"""
        # Target retention level: 80%
        target_retention = 0.8
        intervals = []
        
        func = forgetting_curve['function']
        a = forgetting_curve['parameters']['a']
        b = forgetting_curve['parameters']['b']
        
        day = 0
        while len(intervals) < 5:  # Calculate first 5 review intervals
            day += 1
            current_retention = func(day, a, b)
            
            if current_retention <= target_retention:
                intervals.append(day)
                # Reset after review simulation conceptually means we look for next interval.
                # In Ebbinghaus spacing, intervals typically increase.
                # For simplicity here, we assume standard spaced repetition multipliers.
                day = int(day * 2.5)  
                
        return intervals
