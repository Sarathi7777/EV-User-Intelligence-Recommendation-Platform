import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pickle

def create_mock_driving_data():
    """Create mock driving pattern data for demonstration."""
    n_users = 100
    
    # Mock features: [avg_distance, avg_speed, charging_frequency, eco_score]
    driving_patterns = np.random.rand(n_users, 4)
    
    # Normalize features
    scaler = StandardScaler()
    driving_patterns_scaled = scaler.fit_transform(driving_patterns)
    
    return driving_patterns_scaled, scaler

def train_clustering_model():
    """Train a KMeans clustering model for user driving patterns."""
    print("Creating mock driving pattern data...")
    driving_patterns, scaler = create_mock_driving_data()
    
    print("Training KMeans clustering model...")
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(driving_patterns)
    
    print("Saving clustering model...")
    model_data = {
        'kmeans': kmeans,
        'scaler': scaler,
        'n_clusters': 3
    }
    
    with open('models/clustering_model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print("Clustering model saved to models/clustering_model.pkl")
    return kmeans, clusters

def classify_user_pattern(user_features):
    """Classify a user's driving pattern."""
    try:
        with open('models/clustering_model.pkl', 'rb') as f:
            model_data = pickle.load(f)
        
        kmeans = model_data['kmeans']
        scaler = model_data['scaler']
        
        # Scale user features
        user_scaled = scaler.transform([user_features])
        
        # Predict cluster
        cluster = kmeans.predict(user_scaled)[0]
        
        cluster_names = ['Eco-Friendly', 'Moderate', 'High-Usage']
        return cluster_names[cluster]
        
    except FileNotFoundError:
        return "Unknown"

if __name__ == "__main__":
    train_clustering_model() 