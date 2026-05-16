import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Any

def flatten_dict(d: dict, parent_key: str = '', sep: str = '_') -> dict:
    """Flatten a nested dictionary."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


class LearningStyleClassifier:
    """
    Classifies learner's primary and secondary learning styles based on their
    interactions, assessments, and behavioral events.
    """
    def __init__(self):
        import os
        import pickle
        from app.config import settings
        
        self.model_file = os.path.join(settings.MODEL_PATH, 'learning_style_model.pkl')
        self.scaler_file = os.path.join(settings.MODEL_PATH, 'learning_style_scaler.pkl')
        
        self.is_trained = False
        self.model = None
        self.scaler = None
        self._load_model()
        
    def _load_model(self):
        """Load trained model and scaler from disk, or initialize defaults."""
        import os
        import pickle
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import StandardScaler
        
        if os.path.exists(self.model_file) and os.path.exists(self.scaler_file):
            try:
                with open(self.model_file, 'rb') as f:
                    self.model = pickle.load(f)
                with open(self.scaler_file, 'rb') as f:
                    self.scaler = pickle.load(f)
                self.is_trained = True
                print("LearningStyleClassifier: Loaded trained model from disk.")
            except Exception as e:
                print(f"LearningStyleClassifier: Failed to load model ({e}). Initializing defaults.")
                self.model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
                self.scaler = StandardScaler()
        else:
            print("LearningStyleClassifier: No trained model found. Initializing defaults.")
            self.model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
            self.scaler = StandardScaler()

    def _extract_content_features(self, interactions: List[Any]) -> Dict[str, Any]:
        """Extract features based on content type interactions."""
        # This is a simplified extraction based on the spec
        features = {
            'video_engagement': {'avg_completion_rate': 0.0, 'avg_watch_time': 0.0, 'rewatch_frequency': 0, 'engagement_score': 0.0},
            'text_engagement': {'avg_completion_rate': 0.0, 'avg_watch_time': 0.0, 'rewatch_frequency': 0, 'engagement_score': 0.0},
            'audio_engagement': {'avg_completion_rate': 0.0, 'avg_watch_time': 0.0, 'rewatch_frequency': 0, 'engagement_score': 0.0},
            'interactive_engagement': {'avg_completion_rate': 0.0, 'avg_watch_time': 0.0, 'rewatch_frequency': 0, 'engagement_score': 0.0}
        }
        # In a real scenario, we'd aggregate over the `interactions` list
        return features

    def _extract_performance_features(self, assessments: List[Any]) -> Dict[str, Any]:
        """Extract features based on performance by content type."""
        features = {}
        for content_type in ['visual', 'auditory', 'textual', 'interactive']:
            features[f'{content_type}_performance'] = {
                'avg_score': 0.0,
                'completion_rate': 0.0,
                'time_efficiency': 0.0,
                'retention_score': 0.0
            }
        return features

    def _extract_behavioral_features(self, behavioral_events: List[Any]) -> Dict[str, Any]:
        """Extract features based on detailed behavioral interactions."""
        return {
            'visual_indicators': {'image_hover_time': 0.0, 'diagram_interaction': 0},
            'auditory_indicators': {'audio_playback_preference': 0.0, 'read_aloud_usage': 0},
            'kinesthetic_indicators': {'interactive_element_usage': 0, 'simulation_engagement': 0.0},
            'reading_writing_indicators': {'note_taking_frequency': 0, 'text_highlighting': 0}
        }

    def prepare_features(self, learner_data: Any) -> List[float]:
        """Extract and prepare features for classification."""
        content_features = self._extract_content_features(getattr(learner_data, 'interactions', []))
        performance_features = self._extract_performance_features(getattr(learner_data, 'assessments', []))
        behavioral_features = self._extract_behavioral_features(getattr(learner_data, 'events', []))
        
        # Combine all features
        features = {**content_features, **performance_features, **behavioral_features}
        
        # Flatten nested dictionaries and return values in a fixed order
        flat_features = flatten_dict(features)
        
        # Sort keys to ensure consistent order
        return [float(flat_features[k]) for k in sorted(flat_features.keys())]

    def train(self, training_data: List[Any], labels: List[str]):
        """Train the learning style classifier."""
        X = [self.prepare_features(data) for data in training_data]
        if not X:
            return
            
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, labels)
        self.is_trained = True
        return self.model

    def predict(self, learner_data: Any) -> Dict[str, Any]:
        """Predict learning style with confidence scores."""
        # If model is not trained yet, return a default heuristic-based prediction
        if not self.is_trained:
            return {
                'primary': 'visual',
                'secondary': 'reading_writing',
                'scores': {'visual': 0.5, 'auditory': 0.1, 'kinesthetic': 0.2, 'reading_writing': 0.2},
                'confidence': 0.5,
                'is_multimodal': False
            }

        features = self.prepare_features(learner_data)
        features_scaled = self.scaler.transform([features])
        
        # Get probability scores for each class
        probabilities = self.model.predict_proba(features_scaled)[0]
        learning_styles = self.model.classes_
        
        style_scores = dict(zip(learning_styles, probabilities))
        
        # Determine primary and secondary styles
        sorted_styles = sorted(style_scores.items(), key=lambda x: x[1], reverse=True)
        primary_style = sorted_styles[0][0]
        secondary_style = sorted_styles[1][0] if len(sorted_styles) > 1 else primary_style
        
        return {
            'primary': primary_style,
            'secondary': secondary_style,
            'scores': style_scores,
            'confidence': sorted_styles[0][1],
            **self.detect_multimodal_preference(style_scores)
        }

    def detect_multimodal_preference(self, style_scores: Dict[str, float], threshold: float = 0.3) -> Dict[str, Any]:
        """Detect if learner benefits from multiple learning styles."""
        high_scores = [style for style, score in style_scores.items() if score > threshold]
        
        if len(high_scores) > 1:
            return {
                'is_multimodal': True,
                'preferred_styles': high_scores,
                'recommendation': 'combine_multiple_formats'
            }
        else:
            # Fallback to primary style if dict is empty
            primary = max(style_scores, key=style_scores.get) if style_scores else 'visual'
            return {
                'is_multimodal': False,
                'preferred_styles': [primary],
                'recommendation': 'focus_on_primary_style'
            }
