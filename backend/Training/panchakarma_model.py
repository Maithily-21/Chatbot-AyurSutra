"""
Panchakarma Therapy Recommendation Engine
Maps Dosha imbalances to appropriate Panchakarma treatments
"""
import os
import pickle

# Panchakarma therapy recommendations based on Dosha
PANCHAKARMA_RECOMMENDATIONS = {
    'vata': {
        'primary': ['Basti', 'Nasya'],
        'secondary': ['Abhyanga', 'Shirodhara'],
        'contraindications': ['Vamana', 'Virechana'],
        'description': 'Vata dosha benefits most from Basti (medicated enema) and Nasya (nasal administration) to balance the air and ether elements.',
        'dietary': {
            'favor': ['Warm, cooked foods', 'Ghee', 'Nuts', 'Root vegetables', 'Sweet, sour, salty tastes'],
            'avoid': ['Raw foods', 'Cold drinks', 'Dry foods', 'Bitter and astringent tastes']
        },
        'lifestyle': {
            'routine': 'Maintain regular daily routine, early bedtime, warm oil massage',
            'yoga': 'Gentle, grounding poses, slow movements',
            'pranayama': 'Nadi Shodhana, Bhramari'
        }
    },
    'pitta': {
        'primary': ['Virechana', 'Raktamokshana'],
        'secondary': ['Shirodhara', 'Takradhara'],
        'contraindications': ['Vamana (in excess)'],
        'description': 'Pitta dosha responds well to Virechana (purgation therapy) and Raktamokshana (bloodletting) to eliminate excess fire and water elements.',
        'dietary': {
            'favor': ['Cooling foods', 'Sweet fruits', 'Dairy (moderate)', 'Bitter and astringent tastes'],
            'avoid': ['Spicy foods', 'Alcohol', 'Sour foods', 'Hot beverages', 'Pungent tastes']
        },
        'lifestyle': {
            'routine': 'Avoid midday sun, cool environment, moderate exercise',
            'yoga': 'Cooling poses, forward bends, moon salutations',
            'pranayama': 'Sheetali, Sheetkari, Chandra Bhedana'
        }
    },
    'kapha': {
        'primary': ['Vamana', 'Virechana'],
        'secondary': ['Udvartana', 'Swedana'],
        'contraindications': ['Basti (in excess)'],
        'description': 'Kapha dosha requires Vamana (therapeutic emesis) and Virechana to reduce excess earth and water elements.',
        'dietary': {
            'favor': ['Light, warm foods', 'Spices', 'Honey', 'Bitter and pungent tastes', 'Legumes'],
            'avoid': ['Heavy foods', 'Dairy', 'Sweet foods', 'Oily foods', 'Cold drinks']
        },
        'lifestyle': {
            'routine': 'Early rising, vigorous exercise, active lifestyle',
            'yoga': 'Dynamic sequences, sun salutations, backbends',
            'pranayama': 'Kapalabhati, Bhastrika, Surya Bhedana'
        }
    }
}

def get_panchakarma_recommendations(dosha_results):
    """
    Get Panchakarma therapy recommendations based on dosha assessment
    
    Args:
        dosha_results: Dictionary with dosha percentages and dominant dosha
        
    Returns:
        Dictionary with therapy recommendations
    """
    dominant = dosha_results.get('dominant_dosha', 'vata')
    secondary = dosha_results.get('secondary_dosha')
    percentages = dosha_results.get('percentages', {})
    
    # Get primary recommendations for dominant dosha
    recommendations = PANCHAKARMA_RECOMMENDATIONS[dominant].copy()
    
    # Add secondary dosha considerations if significant
    if secondary and percentages.get(secondary, 0) > 30:
        secondary_recs = PANCHAKARMA_RECOMMENDATIONS[secondary]
        # Combine therapies, avoiding contraindications
        combined_primary = list(set(recommendations['primary'] + secondary_recs['primary']))
        combined_secondary = list(set(recommendations['secondary'] + secondary_recs['secondary']))
        
        # Remove contraindications
        contraindications = set(recommendations.get('contraindications', []) + 
                               secondary_recs.get('contraindications', []))
        combined_primary = [t for t in combined_primary if t not in contraindications]
        combined_secondary = [t for t in combined_secondary if t not in contraindications]
        
        recommendations['primary'] = combined_primary[:2]  # Limit to top 2
        recommendations['secondary'] = combined_secondary[:2]
    
    # Add therapy details
    therapy_details = {
        'Vamana': {
            'description': 'Therapeutic emesis using medicated substances to eliminate excess Kapha dosha from the upper body.',
            'duration': '7-15 days',
            'benefits': 'Clears respiratory tract, improves digestion, reduces phlegm',
            'precautions': 'Not recommended for Vata-dominant individuals, pregnant women, elderly'
        },
        'Virechana': {
            'description': 'Purgation therapy using herbal laxatives to cleanse the intestines and eliminate Pitta dosha.',
            'duration': '7-15 days',
            'benefits': 'Detoxifies liver, improves skin health, balances metabolism',
            'precautions': 'Avoid in severe weakness, during menstruation, certain medical conditions'
        },
        'Basti': {
            'description': 'Medicated enema therapy using herbal oils and decoctions to balance Vata dosha and nourish tissues.',
            'duration': '8-30 days',
            'benefits': 'Strengthens colon, improves elimination, calms nervous system',
            'precautions': 'Not recommended during acute illness, certain digestive disorders'
        },
        'Nasya': {
            'description': 'Nasal administration of medicated oils to cleanse and nourish the head and neck region.',
            'duration': '7-14 days',
            'benefits': 'Clears sinuses, improves voice, enhances mental clarity',
            'precautions': 'Avoid after meals, during acute cold, certain conditions'
        },
        'Raktamokshana': {
            'description': 'Bloodletting therapy to eliminate toxins and excess Pitta from the blood.',
            'duration': 'As needed',
            'benefits': 'Purifies blood, treats skin conditions, reduces inflammation',
            'precautions': 'Requires expert supervision, not for everyone'
        },
        'Abhyanga': {
            'description': 'Full body oil massage with warm medicated oils to balance Vata and promote relaxation.',
            'duration': '45-60 minutes per session',
            'benefits': 'Nourishes skin, calms nervous system, improves circulation',
            'precautions': 'Avoid on full stomach, certain skin conditions'
        },
        'Shirodhara': {
            'description': 'Continuous pouring of warm medicated oil on the forehead to calm the mind.',
            'duration': '30-45 minutes per session',
            'benefits': 'Reduces stress, improves sleep, balances all doshas',
            'precautions': 'Avoid with certain head conditions'
        },
        'Udvartana': {
            'description': 'Dry powder massage to reduce Kapha and improve circulation.',
            'duration': '30-45 minutes per session',
            'benefits': 'Reduces excess weight, improves skin tone, stimulates metabolism',
            'precautions': 'Avoid on sensitive skin'
        },
        'Swedana': {
            'description': 'Herbal steam therapy to induce sweating and eliminate toxins.',
            'duration': '15-30 minutes per session',
            'benefits': 'Opens pores, improves circulation, reduces stiffness',
            'precautions': 'Avoid in high blood pressure, certain conditions'
        },
        'Takradhara': {
            'description': 'Pouring of medicated buttermilk on forehead, beneficial for Pitta conditions.',
            'duration': '30-45 minutes per session',
            'benefits': 'Cools the system, reduces inflammation, calms Pitta',
            'precautions': 'Avoid in cold conditions'
        }
    }
    
    # Add detailed information for recommended therapies
    recommended_therapies = []
    for therapy_name in recommendations['primary']:
        if therapy_name in therapy_details:
            therapy_info = therapy_details[therapy_name].copy()
            therapy_info['name'] = therapy_name
            recommended_therapies.append(therapy_info)
    
    recommendations['therapy_details'] = recommended_therapies
    
    return recommendations

def save_panchakarma_model():
    """Save Panchakarma recommendations model"""
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'Models')
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, 'panchakarma_recommendations.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump({
            'recommendations': PANCHAKARMA_RECOMMENDATIONS,
            'therapy_details': {}
        }, f)
    
    print(f"Panchakarma recommendations saved to {model_path}")
    return model_path

if __name__ == "__main__":
    save_panchakarma_model()

