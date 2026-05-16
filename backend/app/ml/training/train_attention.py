import os
import pickle
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from app.config import settings

def generate_attention_data(num_samples=1000):
    """Generate synthetic data for attention span prediction"""
    X = []
    y = []
    
    for _ in range(num_samples):
        # Features: time_of_day, day_of_week, content_difficulty, historical_avg, recent_sleep, session_num
        time_of_day = np.random.randint(0, 24)
        day_of_week = np.random.randint(0, 7)
        content_diff = np.random.uniform(0.1, 1.0)
        hist_avg = np.random.uniform(10, 60) # 10 to 60 minutes
        recent_sleep = np.random.uniform(4, 10) # 4 to 10 hours
        session_num = np.random.randint(1, 5)
        
        features = [time_of_day, day_of_week, content_diff, hist_avg, recent_sleep, session_num]
        
        # Base attention span is close to historical average
        base_span = hist_avg
        
        # Adjust based on factors
        if time_of_day < 6 or time_of_day > 22:
            base_span *= 0.7 # Less attention late at night
            
        if recent_sleep < 6:
            base_span *= 0.8 # Less attention if sleep deprived
            
        base_span -= (content_diff * 5) # Harder content = lower sustained attention span
        base_span -= (session_num * 2) # Fatigue over multiple sessions
        
        # Add noise
        span = base_span + np.random.normal(0, 3)
        span = max(5.0, min(span, 120.0)) # Clip between 5 and 120 minutes
        
        X.append(features)
        y.append(span)
        
    return np.array(X), np.array(y)

def train_and_save_model():
    print("Generating synthetic attention data...")
    X, y = generate_attention_data(2000)
    
    print("Training Gradient Boosting Regressor (fallback for LSTM)...")
    model = GradientBoostingRegressor(
        n_estimators=100,
        max_depth=5,
        random_state=42
    )
    scaler = StandardScaler()
    
    X_scaled = scaler.fit_transform(X)
    model.fit(X_scaled, y)
    
    # Save models
    os.makedirs(settings.MODEL_PATH, exist_ok=True)
    model_file = os.path.join(settings.MODEL_PATH, 'attention_model.pkl')
    scaler_file = os.path.join(settings.MODEL_PATH, 'attention_scaler.pkl')
    
    with open(model_file, 'wb') as f:
        pickle.dump(model, f)
        
    with open(scaler_file, 'wb') as f:
        pickle.dump(scaler, f)
        
    print(f"Attention model and scaler saved to {settings.MODEL_PATH}")

if __name__ == "__main__":
    train_and_save_model()
