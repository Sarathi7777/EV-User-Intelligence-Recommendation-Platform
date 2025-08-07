import numpy as np
import pickle
from models.recommendation import create_simple_recommendation_model

def train_recommendation_model():
    """Train a simple collaborative filtering recommendation model."""
    print("Creating mock user-item interaction data...")
    
    print("Training collaborative filtering model...")
    model_data = create_simple_recommendation_model()
    
    print("Model saved to models/recommendation_model.pkl")
    return model_data

if __name__ == "__main__":
    train_recommendation_model() 