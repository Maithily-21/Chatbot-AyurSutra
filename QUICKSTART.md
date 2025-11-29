# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run setup (downloads NLTK data and trains models)
python setup.py

# Start the server
python app.py
```

Backend will run on `http://127.0.0.1:8000`

### Step 2: Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:5173`

### Step 3: Access the Application

1. Open your browser
2. Navigate to `http://localhost:5173`
3. Click "Begin Your Assessment"
4. Start chatting with AyurSutra Bot!

## 📝 Notes

- Make sure both servers are running simultaneously
- Backend must be running before starting the frontend
- If models aren't trained, run `python backend/setup.py` first
- Check browser console for any connection errors

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (needs 3.10+)
- Ensure virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`
- Train models: `python setup.py`

### Frontend won't connect
- Verify backend is running on port 8000
- Check `.env` file has correct URLs
- Clear browser cache
- Check browser console for errors

### Models not found
- Run `python backend/setup.py`
- Or manually train: `python backend/run_training.py`
- Check `backend/Models/` directory exists

## ✅ Verification

1. Backend health check: Visit `http://127.0.0.1:8000/health`
2. API docs: Visit `http://127.0.0.1:8000/docs`
3. Frontend: Visit `http://localhost:5173`

Happy coding! 🌿

