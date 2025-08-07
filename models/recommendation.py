import os
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

MODEL_PATH = os.getenv("RECOMMENDATION_MODEL_PATH", "models/recommendation_model.pkl")

def create_simple_recommendation_model():
    """Create a simple collaborative filtering model using cosine similarity."""
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
    
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model_data, f)
    
    return model_data

def load_recommendation_model():
    """Load the recommendation model."""
    try:
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        # Create model if it doesn't exist
        return create_simple_recommendation_model()

def recommend_stations(model_data, user_id: int, num_recs: int = 5):
    """Recommend stations for a user using collaborative filtering."""
    if user_id >= model_data['n_users']:
        # Return random recommendations for new users
        return np.random.choice(model_data['n_items'], num_recs, replace=False).tolist()
    
    # Get user's interaction history
    user_interactions = model_data['interactions'][user_id]
    
    # Find similar users
    user_similarities = cosine_similarity([user_interactions], model_data['interactions'])[0]
    similar_users = np.argsort(user_similarities)[::-1][1:6]  # Top 5 similar users
    
    # Get recommendations from similar users
    recommendations = []
    for similar_user in similar_users:
        similar_user_items = np.where(model_data['interactions'][similar_user] == 1)[0]
        recommendations.extend(similar_user_items)
    
    # Remove items user already interacted with
    user_items = np.where(user_interactions == 1)[0]
    recommendations = [r for r in recommendations if r not in user_items]
    
    # Return top N unique recommendations
    unique_recs = list(dict.fromkeys(recommendations))[:num_recs]
    
    # Pad with random if not enough
    while len(unique_recs) < num_recs:
        random_item = np.random.randint(0, model_data['n_items'])
        if random_item not in unique_recs:
            unique_recs.append(random_item)
    
    return unique_recs[:num_recs]