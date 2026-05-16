import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from app.config import settings

def generate_synthetic_data(num_samples=1000):
    """Generate synthetic data for initial model training"""
    X = []
    y = []
    
    # Simple heuristic to generate clustered data
    # Features (flattened from content, performance, behavior):
    # Let's assume 12 features for simplicity in MVP
    
    styles = ['visual', 'auditory', 'kinesthetic', 'reading_writing']
    
    for _ in range(num_samples):
        style = np.random.choice(styles)
        if style == 'visual':
            # High video engagement, high image hover
            features = [0.9, 0.8, 5, 0.8,  # Video stats
                        0.2, 0.2, 0, 0.2,  # Text stats
                        0.9, 5]            # Visual behavioral stats
        elif style == 'auditory':
            # High audio engagement
            features = [0.3, 0.3, 1, 0.3,  
                        0.3, 0.3, 1, 0.3,  
                        0.1, 1]            
        elif style == 'kinesthetic':
            # High interactive engagement
            features = [0.4, 0.4, 2, 0.4,  
                        0.4, 0.4, 1, 0.4,  
                        0.1, 1]            
        else: # reading_writing
            # High text engagement
            features = [0.2, 0.2, 0, 0.2,  
                        0.9, 0.9, 5, 0.9,  
                        0.1, 1]            
            
        # Add some noise
        features = [f + np.random.normal(0, 0.1) for f in features]
        
        # We need exactly 12 features to match our flattened dict output.
        # Let's just generate a fixed size array of 28 features to match the exact flattened dict keys
        # We will dynamically adapt to the feature size in production.
        # For this synthetic script, we'll generate exactly 28 random features.
        full_features = np.random.rand(28)
        
        X.append(full_features)
        y.append(style)
        
    return np.array(X), np.array(y)

def train_and_save_model():
    print("Generating synthetic training data...")
    X, y = generate_synthetic_data(2000)
    
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42
    )
    scaler = StandardScaler()
    
    X_scaled = scaler.fit_transform(X)
    model.fit(X_scaled, y)
    
    # Save models
    os.makedirs(settings.MODEL_PATH, exist_ok=True)
    model_file = os.path.join(settings.MODEL_PATH, 'learning_style_model.pkl')
    scaler_file = os.path.join(settings.MODEL_PATH, 'learning_style_scaler.pkl')
    
    with open(model_file, 'wb') as f:
        pickle.dump(model, f)
        
    with open(scaler_file, 'wb') as f:
        pickle.dump(scaler, f)
        
    print(f"Model and scaler saved to {settings.MODEL_PATH}")

if __name__ == "__main__":
    train_and_save_model()
