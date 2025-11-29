import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pickle
import os

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger', quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    """Clean and preprocess text for NLP"""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return ' '.join(tokens)

def extract_keywords(text):
    """Extract keywords from user input"""
    cleaned = clean_text(text)
    tokens = word_tokenize(cleaned)
    return tokens

def match_intent(user_input, intents_data):
    """Simple intent matching based on keywords"""
    cleaned_input = clean_text(user_input)
    input_words = set(cleaned_input.split())
    
    best_match = None
    best_score = 0
    
    for intent in intents_data:
        patterns = intent.get('patterns', [])
        for pattern in patterns:
            pattern_words = set(clean_text(pattern).split())
            # Calculate similarity
            common_words = input_words.intersection(pattern_words)
            if common_words:
                score = len(common_words) / max(len(input_words), len(pattern_words))
                if score > best_score:
                    best_score = score
                    best_match = intent
    
    return best_match if best_score > 0.3 else None

def extract_dosha_keywords(text):
    """Extract dosha-related keywords from text"""
    dosha_keywords = {
        'vata': ['thin', 'light', 'dry', 'cold', 'irregular', 'anxious', 'creative', 'quick'],
        'pitta': ['medium', 'warm', 'oily', 'sharp', 'intense', 'ambitious', 'irritable', 'perfectionist'],
        'kapha': ['heavy', 'thick', 'smooth', 'slow', 'calm', 'stable', 'grounded', 'loving']
    }
    
    cleaned = clean_text(text)
    found_doshas = []
    
    for dosha, keywords in dosha_keywords.items():
        for keyword in keywords:
            if keyword in cleaned:
                found_doshas.append(dosha)
                break
    
    return found_doshas

