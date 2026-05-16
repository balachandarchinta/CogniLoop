import statistics
from typing import List, Dict, Any

class ComprehensionSpeedAssessor:
    """Assesses learner's comprehension speed."""
    def __init__(self):
        self.speed_categories = {
            'slow': (0, 0.7),
            'moderate': (0.7, 1.3),
            'fast': (1.3, float('inf'))
        }
    
    def assess_speed(self, learner_data: Any) -> Dict[str, Any]:
        """Assess learner's comprehension speed"""
        # 1. Content completion speed
        content_speed = self.calculate_content_speed(getattr(learner_data, 'content_interactions', []))
        
        # 2. Quiz performance speed
        quiz_speed = self.calculate_quiz_speed(getattr(learner_data, 'assessments', []))
        
        # 3. Concept mastery rate
        mastery_speed = self.calculate_mastery_speed(getattr(learner_data, 'learning_progress', []))
        
        # 4. Question response speed
        response_speed = self.calculate_response_speed(getattr(learner_data, 'questions', []))
        
        # Weighted average
        overall_speed = (
            content_speed * 0.3 +
            quiz_speed * 0.3 +
            mastery_speed * 0.25 +
            response_speed * 0.15
        )
        
        # Categorize speed
        speed_category = self.categorize_speed(overall_speed)
        
        return {
            'speed_score': overall_speed,
            'category': speed_category,
            'components': {
                'content_speed': content_speed,
                'quiz_speed': quiz_speed,
                'mastery_speed': mastery_speed,
                'response_speed': response_speed
            }
        }
    
    def calculate_content_speed(self, interactions: List[Any]) -> float:
        """Calculate speed of content consumption"""
        speeds = []
        for interaction in interactions:
            expected_time = getattr(interaction.content, 'estimated_duration', 1.0)
            actual_time = getattr(interaction, 'time_spent', 1.0)
            
            speed_ratio = expected_time / actual_time if actual_time > 0 else 0
            comprehension_score = getattr(interaction, 'comprehension_score', 1.0)
            
            if comprehension_score > 0.6:
                speeds.append(speed_ratio)
                
        return statistics.mean(speeds) if speeds else 1.0
    
    def calculate_quiz_speed(self, assessments: List[Any]) -> float:
        """Calculate quiz completion speed with accuracy consideration"""
        speeds = []
        for assessment in assessments:
            questions = getattr(assessment, 'questions', [])
            num_questions = len(questions) if questions else 1
            time_taken = getattr(assessment, 'time_taken', 60.0)
            
            time_per_question = time_taken / num_questions
            expected_time_per_question = 60.0  # seconds
            
            speed_ratio = expected_time_per_question / time_per_question if time_per_question > 0 else 1.0
            
            score = getattr(assessment, 'score', 100)
            accuracy_factor = score / 100.0
            adjusted_speed = speed_ratio * accuracy_factor
            
            speeds.append(adjusted_speed)
            
        return statistics.mean(speeds) if speeds else 1.0
        
    def calculate_mastery_speed(self, learning_progress: List[Any]) -> float:
        """Stub for mastery speed"""
        return 1.0

    def calculate_response_speed(self, questions: List[Any]) -> float:
        """Stub for response speed"""
        return 1.0

    def categorize_speed(self, speed_score: float) -> str:
        """Categorize comprehension speed"""
        for category, (min_val, max_val) in self.speed_categories.items():
            if min_val <= speed_score < max_val:
                return category
        return 'moderate'
