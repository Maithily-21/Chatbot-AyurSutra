"""
Chatbot NLP Model Training
Simple intent classification using keyword matching and basic ML
"""
import json
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np

def load_intents():
    """Load intents from JSON file"""
    intents_path = os.path.join(os.path.dirname(__file__), 'intents.json')
    with open(intents_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def prepare_training_data(intents_data):
    """Prepare training data from intents"""
    X = []
    y = []
    
    for intent in intents_data['intents']:
        tag = intent['tag']
        patterns = intent['patterns']
        
        for pattern in patterns:
            X.append(pattern.lower())
            y.append(tag)
    
    return X, y

def train_chatbot_model():
    """Train the chatbot intent classification model"""
    print("Loading intents...")
    intents_data = load_intents()
    
    print("Preparing training data...")
    X, y = prepare_training_data(intents_data)
    
    print(f"Training on {len(X)} samples...")
    
    # Create pipeline with TF-IDF vectorizer and Naive Bayes classifier
    model = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
        ('classifier', MultinomialNB(alpha=0.1))
    ])
    
    model.fit(X, y)
    
    # Save model
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'Models')
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, 'chatbot_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    # Save intents for reference
    intents_path = os.path.join(models_dir, 'intents.pkl')
    with open(intents_path, 'wb') as f:
        pickle.dump(intents_data, f)
    
    print(f"Model saved to {model_path}")
    print("Chatbot model training completed!")
    
    return model, intents_data

if __name__ == "__main__":
    train_chatbot_model()

