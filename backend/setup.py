"""
Setup script for AyurSutra backend
Initializes database and trains models
"""
import os
import sys
import subprocess

def download_nltk_data():
    """Download required NLTK data"""
    print("Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        print("✓ NLTK data downloaded successfully")
    except Exception as e:
        print(f"✗ Error downloading NLTK data: {e}")
        return False
    return True

def train_models():
    """Train all ML models"""
    print("\nTraining ML models...")
    
    models = [
        ('Training/botmodel.py', 'Chatbot model'),
        ('Training/prakritimodel.py', 'Prakriti model'),
        ('Training/panchakarma_model.py', 'Panchakarma model')
    ]
    
    for script, name in models:
        print(f"\nTraining {name}...")
        try:
            result = subprocess.run([sys.executable, script], 
                                  capture_output=True, 
                                  text=True,
                                  cwd=os.path.dirname(__file__))
            if result.returncode == 0:
                print(f"✓ {name} trained successfully")
            else:
                print(f"✗ Error training {name}: {result.stderr}")
                return False
        except Exception as e:
            print(f"✗ Error running {script}: {e}")
            return False
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\nCreating directories...")
    directories = ['Models', 'reports']
    base_dir = os.path.dirname(__file__)
    
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"✓ Created {directory}/ directory")

def main():
    """Main setup function"""
    print("=" * 50)
    print("AyurSutra Backend Setup")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Download NLTK data
    if not download_nltk_data():
        print("\n⚠ Warning: NLTK data download failed. Some features may not work.")
    
    # Train models
    if not train_models():
        print("\n✗ Model training failed. Please check the errors above.")
        return False
    
    print("\n" + "=" * 50)
    print("✓ Setup completed successfully!")
    print("=" * 50)
    print("\nYou can now run the server with: python app.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

