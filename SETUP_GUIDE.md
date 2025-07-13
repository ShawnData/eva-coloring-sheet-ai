# Eva's Coloring Sheet AI - Setup Guide

This guide will help you install React and get both the backend and frontend running.

## Prerequisites

### 1. Install Node.js

**Windows:**
1. Go to https://nodejs.org/
2. Download the "LTS" (Long Term Support) version
3. Run the installer and follow the installation wizard
4. Restart your terminal/command prompt after installation

**Verify Installation:**
```bash
node --version
npm --version
```

Both commands should return version numbers.

## Quick Setup (Git Bash/Linux/macOS)

### Option 1: Using Bash Scripts (Recommended)

1. **Install Node.js** (see above)

2. **Run the setup script:**
   ```bash
   ./setup_react_frontend.sh
   ```

3. **Start the backend** (in a new terminal):
   ```bash
   ./start_backend.sh
   ```

4. **Start the frontend** (in another terminal):
   ```bash
   ./start_frontend.sh
   ```

5. **Open your browser** to: http://localhost:3000

### Option 2: Manual Setup

1. **Install Node.js** (see above)

2. **Install React dependencies:**
   ```bash
   cd frontend
   npm install
   ```

3. **Start the backend** (in a new terminal):
   ```bash
   python api_server.py
   ```

4. **Start the frontend** (in another terminal):
   ```bash
   cd frontend
   npm start
   ```

5. **Open your browser** to: http://localhost:3000

## Troubleshooting

### Node.js Installation Issues

**If `node --version` doesn't work:**
1. Make sure you restarted your terminal after installation
2. Check if Node.js is in your PATH environment variable
3. Try running the installer as administrator

**If npm install fails:**
1. Make sure you have a stable internet connection
2. Try running: `npm cache clean --force`
3. Delete the `node_modules` folder and run `npm install` again

### Backend Issues

**If the API server won't start:**
1. Make sure all Python dependencies are installed:
   ```bash
   pip install flask flask-cors
   ```
2. Check that your `.env` file has the correct OpenAI API key
3. Make sure port 5000 is not already in use

### Frontend Issues

**If the React app won't start:**
1. Make sure you're in the `frontend` directory
2. Try deleting `node_modules` and running `npm install` again
3. Check that port 3000 is not already in use

**If you get CORS errors:**
1. Make sure the backend is running on port 5000
2. Check that the frontend is trying to connect to the correct URL

## File Structure

```
eva-coloring-sheet-ai/
├── api_server.py              # Flask API backend
├── start_backend.sh           # Backend startup script
├── start_frontend.sh          # Frontend startup script
├── setup_react_frontend.sh    # React setup script
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── VoiceRecorder.js
│   │   │   ├── ChatHistory.js
│   │   │   └── ImageDisplay.js
│   │   └── App.js
│   └── package.json
└── src/                       # Python backend code
```

## What Each Component Does

- **Backend (api_server.py)**: Handles voice processing and AI interactions
- **Frontend (React)**: Provides the user interface with toggle recording
- **VoiceRecorder**: Handles microphone access and recording
- **ChatHistory**: Displays conversation between user and AI
- **ImageDisplay**: Shows generated coloring sheets

## Next Steps

Once everything is running:
1. Click the "🎤 TALK" button to start recording
2. Speak your request (e.g., "I want a cat coloring sheet")
3. Click "🎤 STOP" to stop recording and send your request
4. Wait for the AI to generate your coloring sheet!

Enjoy creating beautiful coloring sheets with Eva's AI! 🎨✨ 