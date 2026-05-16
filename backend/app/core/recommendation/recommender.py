import random
from typing import List, Dict, Any, Optional
from uuid import UUID

class RecommendationEngine:
    """
    Generates personalized content recommendations and learning paths.
    """
    def __init__(self):
        self.max_recommendations = 5
        
    def score_content(self, content: Dict[str, Any], profile: Dict[str, Any], adaptation_directive: Dict[str, Any]) -> float:
        """
        Calculate a matching score (0.0 to 1.0) for a piece of content.
        
        Factors:
        - Difficulty match
        - Format match (Learning Style)
        - Topic interest (from profile behavioral patterns)
        """
        score = 0.0
        
        # 1. Difficulty Match (30%)
        target_diff = adaptation_directive.get('difficulty', {}).get('label', 'Intermediate').lower()
        if content.get('difficulty_level', '').lower() == target_diff:
            score += 0.3
        elif content.get('difficulty_level', '').lower() == 'beginner' and target_diff == 'intermediate':
            score += 0.15 # Allow slightly easier content
            
        # 2. Format Match (40%)
        primary_style = profile.get('learning_style', {}).get('primary', 'visual').lower()
        content_format = content.get('content_format', '').lower()
        
        style_format_map = {
            "visual": ["visual", "video", "diagram"],
            "auditory": ["auditory", "audio", "podcast"],
            "kinesthetic": ["interactive", "simulation", "lab"],
            "reading_writing": ["textual", "text", "article"]
        }
        
        if content_format in style_format_map.get(primary_style, []):
            score += 0.4
        elif content.get('content_type', '').lower() in style_format_map.get(primary_style, []):
            score += 0.4
            
        # 3. Topic/Subject Relevance (30%)
        # For MVP, we'll assume the learner is currently pursuing a specific subject
        score += 0.3 
        
        return score

    def rank_content(self, content_list: List[Dict[str, Any]], profile: Dict[str, Any], adaptation_directive: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Rank a list of content items"""
        scored_items = []
        for item in content_list:
            item['recommendation_score'] = self.score_content(item, profile, adaptation_directive)
            scored_items.append(item)
            
        return sorted(scored_items, key=lambda x: x['recommendation_score'], reverse=True)

    def generate_learning_path(self, 
                              all_content: List[Dict[str, Any]], 
                              completed_content_ids: List[str],
                              profile: Dict[str, Any],
                              adaptation_directive: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Sequences content into a learning path, respecting prerequisites.
        """
        available_content = [c for c in all_content if c['id'] not in completed_content_ids]
        
        # Filter for content where prerequisites are met
        ready_to_learn = []
        for content in available_content:
            prereqs = content.get('prerequisites', []) or []
            if all(p in completed_content_ids for p in prereqs):
                ready_to_learn.append(content)
                
        # Rank the "ready" content
        ranked = self.rank_content(ready_to_learn, profile, adaptation_directive)
        
        return ranked[:self.max_recommendations]
