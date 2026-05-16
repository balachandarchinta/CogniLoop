from typing import Dict, Any, List

class ContentFormatTransformer:
    """
    Recommends content formats and transformations based on learning style.
    """
    def __init__(self):
        self.format_mapping = {
            "visual": ["Video", "Infographic", "Diagram", "Mind Map"],
            "auditory": ["Podcast", "Audio Lecture", "Discussion", "Read Aloud"],
            "kinesthetic": ["Interactive Lab", "Simulation", "Coding Exercise", "Drag & Drop"],
            "reading_writing": ["Article", "Technical Documentation", "Quiz", "Essay"]
        }
        
    def recommend_formats(self, learning_style_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Rank content formats based on learning style scores.
        """
        scores = learning_style_profile.get('scores', {})
        if not scores:
            return [{"format": "Article", "weight": 1.0}]
            
        recommendations = []
        for style, score in scores.items():
            formats = self.format_mapping.get(style, [])
            for fmt in formats:
                recommendations.append({
                    "format": fmt,
                    "relevance_score": score,
                    "style_category": style
                })
                
        # Sort by relevance score
        recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return recommendations[:5] # Return top 5 formats

    def get_transformation_directive(self, primary_style: str) -> str:
        """Instruction for content adaptation"""
        directives = {
            "visual": "Prioritize visual aids and video content. Use color-coded diagrams.",
            "auditory": "Provide audio summaries and encourage verbal reinforcement.",
            "kinesthetic": "Embed interactive simulations and hands-on exercises.",
            "reading_writing": "Provide detailed text-based explanations and structured notes."
        }
        return directives.get(primary_style, "Maintain balanced multi-modal content.")
