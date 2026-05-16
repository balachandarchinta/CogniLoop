import statistics
from typing import List, Dict, Any

def calculate_engagement_score(session_data: Any) -> float:
    """Calculate real-time engagement score (0-1)"""
    # Interaction frequency (normalized)
    interactions_per_minute = getattr(session_data, 'interactions_per_minute', 0)
    interaction_score = min(interactions_per_minute / 5.0, 1.0)
    
    # Scroll behavior (optimal range: 20-80% depth)
    scroll_depth = getattr(session_data, 'scroll_depth', 0.5)
    scroll_score = 1.0 - abs(scroll_depth - 0.5) * 2
    
    # Time on content (compared to expected time)
    actual_time = getattr(session_data, 'actual_time', 1.0)
    expected_time = getattr(session_data, 'expected_time', 1.0)
    
    time_ratio = actual_time / expected_time if expected_time > 0 else 1.0
    time_score = 1.0 if 0.8 <= time_ratio <= 1.2 else max(0.0, 1.0 - abs(time_ratio - 1.0))
    
    # Mouse movement activity
    mouse_movements = getattr(session_data, 'mouse_movements', 0)
    movement_score = min(mouse_movements / 100.0, 1.0)
    
    # Tab focus (penalty for tab switching)
    tab_switches = getattr(session_data, 'tab_switches', 0)
    focus_score = 1.0 - (tab_switches * 0.1)
    
    # Weighted combination
    engagement_score = (
        interaction_score * 0.3 +
        scroll_score * 0.2 +
        time_score * 0.25 +
        movement_score * 0.15 +
        focus_score * 0.1
    )
    
    return max(0.0, min(1.0, engagement_score))


class AttentionSpanAnalyzer:
    """Analyzes attention span by calculating engagement scores over time."""
    def __init__(self):
        import os
        import pickle
        from app.config import settings
        
        self.engagement_threshold = 0.4
        self.window_size = 60  # seconds
        
        self.model_file = os.path.join(settings.MODEL_PATH, 'attention_model.pkl')
        self.scaler_file = os.path.join(settings.MODEL_PATH, 'attention_scaler.pkl')
        
        self.lstm_model = None  # Using GradientBoostingRegressor as MVP fallback
        self.scaler = None
        self.is_trained = False
        self.distraction_detector = DistractionDetector()
        self._load_model()
        
    def _load_model(self):
        """Load trained model and scaler from disk."""
        import os
        import pickle
        from sklearn.ensemble import GradientBoostingRegressor
        from sklearn.preprocessing import StandardScaler
        
        if os.path.exists(self.model_file) and os.path.exists(self.scaler_file):
            try:
                with open(self.model_file, 'rb') as f:
                    self.lstm_model = pickle.load(f)
                with open(self.scaler_file, 'rb') as f:
                    self.scaler = pickle.load(f)
                self.is_trained = True
                print("AttentionSpanAnalyzer: Loaded trained model from disk.")
            except Exception as e:
                print(f"AttentionSpanAnalyzer: Failed to load model ({e}). Initializing defaults.")
                self.lstm_model = GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42)
                self.scaler = StandardScaler()
        else:
            print("AttentionSpanAnalyzer: No trained model found. Initializing defaults.")
            self.lstm_model = GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42)
            self.scaler = StandardScaler()
            
    def analyze_session(self, session_events: List[Any]) -> Dict[str, Any]:
        """Analyze a learning session to determine attention span."""
        if not session_events:
            return {
                'average_attention_span': 0,
                'std_deviation': 0,
                'attention_drops': 0,
                'engagement_timeline': []
            }

        # Calculate engagement scores over time
        engagement_timeline = []
        for i in range(0, len(session_events), self.window_size):
            window_events = session_events[i:i + self.window_size]
            # Create a dummy session_data object representing the window
            class WindowData:
                def __init__(self, events):
                    self.interactions_per_minute = len(events)
                    self.scroll_depth = 0.5
                    self.actual_time = len(events)
                    self.expected_time = len(events)
                    self.mouse_movements = len(events) * 2
                    self.tab_switches = 0
            
            score = calculate_engagement_score(WindowData(window_events))
            # Just grab timestamp from first event if available, else use index
            timestamp = getattr(window_events[0], 'timestamp', i)
            
            engagement_timeline.append({
                'timestamp': timestamp,
                'score': score,
                'duration': len(window_events)
            })
            
        # Detect attention drops
        attention_spans = []
        current_span_start = 0
        
        for i, point in enumerate(engagement_timeline):
            if point['score'] < self.engagement_threshold:
                # Attention dropped
                if i > current_span_start:
                    span_duration = sum(p['duration'] for p in engagement_timeline[current_span_start:i])
                    attention_spans.append(span_duration / 60.0)  # Convert to minutes
                current_span_start = i + 1
                
        # Calculate average attention span
        if attention_spans:
            avg_attention_span = statistics.mean(attention_spans)
            std_attention_span = statistics.stdev(attention_spans) if len(attention_spans) > 1 else 0.0
        else:
            avg_attention_span = len(session_events) / 60.0
            std_attention_span = 0.0
            
        return {
            'average_attention_span': avg_attention_span,
            'std_deviation': std_attention_span,
            'attention_drops': len(attention_spans),
            'engagement_timeline': engagement_timeline,
            'distraction_analysis': self.distraction_detector.detect_distraction(session_events) if session_events else None
        }

class DistractionDetector:
    def __init__(self):
        self.distraction_indicators = {
            'tab_switch': 0.3,
            'rapid_navigation': 0.25,
            'low_scroll_depth': 0.2,
            'no_interaction': 0.15,
            'incomplete_content': 0.1
        }
    
    def detect_distraction(self, session_events: List[Any]) -> Dict[str, Any]:
        """Detect distraction patterns in real-time"""
        # For MVP, we will use simplistic heuristics based on the last few events
        recent_events = session_events[-10:] if len(session_events) >= 10 else session_events
        
        # Heuristic calculations
        tab_switches = sum(1 for e in recent_events if getattr(e, 'type', '') == 'tab_switch')
        avg_time = getattr(recent_events[-1], 'time_spent', 60) if recent_events else 60
        avg_scroll = 0.5
        interactions = len(recent_events)
        
        indicators = {
            'tab_switch': tab_switches > 2,
            'rapid_navigation': avg_time < 30,
            'low_scroll_depth': avg_scroll < 0.3,
            'no_interaction': interactions == 0,
            'incomplete_content': False  # difficult to ascertain just from events without content metadata
        }
        
        # Calculate distraction score
        distraction_score = sum(
            self.distraction_indicators[key] 
            for key, value in indicators.items() 
            if value
        )
        
        # Classify distraction level
        if distraction_score > 0.6:
            level = 'high'
            action = 'immediate_intervention'
        elif distraction_score > 0.3:
            level = 'medium'
            action = 'gentle_reminder'
        else:
            level = 'low'
            action = 'continue_monitoring'
        
        return {
            'distracted': distraction_score > 0.3,
            'level': level,
            'score': distraction_score,
            'indicators': indicators,
            'recommended_action': action
        }

