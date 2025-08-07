#!/usr/bin/env python3
"""
Train ML models for the EV platform
"""

import os
import sys
import pickle
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

def create_recommendation_model():
    """Create a simple collaborative filtering model."""
    print("Creating recommendation model...")
    
    # Mock user-item interaction matrix
    n_users = 100
    n_items = 50
    interactions = np.random.randint(0, 2, (n_users, n_items))
    
    # Calculate similarity matrix
    similarity_matrix = cosine_similarity(interactions.T)
    
    model_data = {
        'interactions': interactions,
        'similarity_matrix': similarity_matrix,
        'n_users': n_users,
        'n_items': n_items
    }
    
    os.makedirs('models', exist_ok=True)
    with open('models/recommendation_model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print("✅ Recommendation model saved to models/recommendation_model.pkl")
    return model_data

def create_clustering_model():
    """Create a KMeans clustering model for user patterns."""
    print("Creating clustering model...")
    
    # Mock driving pattern data
    n_users = 100
    driving_patterns = np.random.rand(n_users, 4)  # [avg_distance, avg_speed, charging_frequency, eco_score]
    
    # Normalize features
    scaler = StandardScaler()
    driving_patterns_scaled = scaler.fit_transform(driving_patterns)
    
    # Train KMeans
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(driving_patterns_scaled)
    
    model_data = {
        'kmeans': kmeans,
        'scaler': scaler,
        'n_clusters': 3
    }
    
    with open('models/clustering_model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print("✅ Clustering model saved to models/clustering_model.pkl")
    return kmeans, clusters

def main():
    print("🤖 Training ML Models for EV Platform")
    print("=" * 50)
    
    # Train recommendation model
    create_recommendation_model()
    
    # Train clustering model
    create_clustering_model()
    
    print("\n🎉 All models trained successfully!")
    print("📁 Models saved in models/ directory")

if __name__ == "__main__":
    main() 