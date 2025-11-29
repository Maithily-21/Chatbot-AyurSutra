"""
Dosha (Prakriti) Classification Model
Determines Vata, Pitta, Kapha scores based on assessment responses
"""
import pickle
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Dosha assessment question weights
DOSHA_QUESTIONS = {
    'vata': {
        'body_frame': {'thin': 3, 'medium': 1, 'heavy': 0},
        'skin_type': {'dry': 3, 'rough': 2, 'normal': 1, 'oily': 0},
        'hair_texture': {'thin': 2, 'dry': 2, 'normal': 1, 'thick': 0},
        'appetite': {'irregular': 3, 'variable': 2, 'regular': 0},
        'digestion': {'irregular': 3, 'variable': 2, 'regular': 0},
        'energy_level': {'variable': 3, 'irregular': 2, 'consistent': 0},
        'sleep': {'light': 3, 'interrupted': 2, 'deep': 0},
        'temperament': {'anxious': 3, 'creative': 2, 'quick': 2, 'calm': 0},
        'stress_response': {'worried': 3, 'anxious': 2, 'calm': 0},
        'weather_preference': {'warm': 3, 'hot': 2, 'cold': 0}
    },
    'pitta': {
        'body_frame': {'medium': 3, 'thin': 1, 'heavy': 1},
        'skin_type': {'oily': 3, 'sensitive': 2, 'normal': 1, 'dry': 0},
        'hair_texture': {'fine': 2, 'oily': 2, 'normal': 1, 'thick': 0},
        'appetite': {'strong': 3, 'regular': 2, 'irregular': 0},
        'digestion': {'strong': 3, 'regular': 2, 'irregular': 0},
        'energy_level': {'high': 3, 'moderate': 2, 'low': 0},
        'sleep': {'moderate': 2, 'light': 1, 'deep': 1},
        'temperament': {'intense': 3, 'ambitious': 2, 'irritable': 2, 'calm': 0},
        'stress_response': {'irritable': 3, 'angry': 2, 'calm': 0},
        'weather_preference': {'cool': 3, 'moderate': 1, 'hot': 0}
    },
    'kapha': {
        'body_frame': {'heavy': 3, 'large': 2, 'medium': 1, 'thin': 0},
        'skin_type': {'oily': 3, 'smooth': 2, 'normal': 1, 'dry': 0},
        'hair_texture': {'thick': 3, 'oily': 2, 'normal': 1, 'thin': 0},
        'appetite': {'regular': 3, 'moderate': 2, 'irregular': 0},
        'digestion': {'slow': 3, 'moderate': 2, 'fast': 0},
        'energy_level': {'low': 3, 'moderate': 2, 'high': 0},
        'sleep': {'deep': 3, 'sound': 2, 'light': 0},
        'temperament': {'calm': 3, 'stable': 2, 'grounded': 2, 'anxious': 0},
        'stress_response': {'calm': 3, 'peaceful': 2, 'anxious': 0},
        'weather_preference': {'warm': 3, 'hot': 2, 'cold': 0}
    }
}

def calculate_dosha_scores(assessment_data):
    """
    Calculate Vata, Pitta, Kapha scores based on assessment responses
    
    Args:
        assessment_data: Dictionary with question-answer pairs
        
    Returns:
        Dictionary with dosha scores and percentages
    """
    scores = {'vata': 0, 'pitta': 0, 'kapha': 0}
    total_weight = {'vata': 0, 'pitta': 0, 'kapha': 0}
    
    for question, answer in assessment_data.items():
        for dosha, questions in DOSHA_QUESTIONS.items():
            if question in questions:
                weights = questions[question]
                if answer in weights:
                    score = weights[answer]
                    scores[dosha] += score
                    total_weight[dosha] += 3  # Max possible score per question
    
    # Normalize scores to percentages
    total_score = sum(scores.values())
    if total_score > 0:
        percentages = {
            'vata': round((scores['vata'] / total_score) * 100, 2),
            'pitta': round((scores['pitta'] / total_score) * 100, 2),
            'kapha': round((scores['kapha'] / total_score) * 100, 2)
        }
    else:
        percentages = {'vata': 33.33, 'pitta': 33.33, 'kapha': 33.33}
    
    # Determine dominant and secondary doshas
    sorted_doshas = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
    dominant_dosha = sorted_doshas[0][0]
    secondary_dosha = sorted_doshas[1][0] if len(sorted_doshas) > 1 else None
    
    return {
        'scores': scores,
        'percentages': percentages,
        'dominant_dosha': dominant_dosha,
        'secondary_dosha': secondary_dosha
    }

def train_prakriti_model():
    """Train a model for dosha prediction (optional enhancement)"""
    # For now, we use rule-based calculation
    # This can be enhanced with ML if we have training data
    print("Prakriti model uses rule-based calculation from Ayurvedic principles.")
    print("Model logic implemented in calculate_dosha_scores() function.")
    
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'Models')
    os.makedirs(models_dir, exist_ok=True)
    
    # Save the question weights for reference
    model_path = os.path.join(models_dir, 'prakriti_weights.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(DOSHA_QUESTIONS, f)
    
    print(f"Prakriti weights saved to {model_path}")
    return DOSHA_QUESTIONS

if __name__ == "__main__":
    train_prakriti_model()

