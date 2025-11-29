"""
Quick script to train all models
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("Training chatbot model...")
from Training.botmodel import train_chatbot_model
train_chatbot_model()

print("\nTraining prakriti model...")
from Training.prakritimodel import train_prakriti_model
train_prakriti_model()

print("\nSaving panchakarma recommendations...")
from Training.panchakarma_model import save_panchakarma_model
save_panchakarma_model()

print("\n✓ All models trained successfully!")

