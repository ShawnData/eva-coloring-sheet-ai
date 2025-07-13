# Eva's Coloring Sheet AI - React Frontend

A beautiful, kid-friendly React frontend for Eva's Coloring Sheet AI with proper voice recording functionality.

## Features

- 🎤 **Toggle Voice Recording** - Click to start, click to stop
- 🎨 **Beautiful UI** - Kid-friendly design with animations
- 💬 **Real-time Chat** - See conversation history
- 🖼️ **Image Display** - View generated coloring sheets
- 📱 **Responsive Design** - Works on desktop and mobile

## Setup

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn
- Python backend running (see main README)

### Installation

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm start
   ```

3. **Open your browser:**
   Navigate to `http://localhost:3000`

## How It Works

### Voice Recording
- **First Click**: Starts recording (button turns red, shows "🎤 STOP")
- **Second Click**: Stops recording and sends to backend
- **Processing**: Button shows "⏳ Processing..." while working
- **Complete**: Button resets to "🎤 TALK" for next recording

### UI Components
- **VoiceRecorder**: Handles microphone access and recording
- **ChatHistory**: Displays conversation with user/assistant messages
- **ImageDisplay**: Shows generated coloring sheets

## Development

### Project Structure
```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── VoiceRecorder.js
│   │   ├── ChatHistory.js
│   │   └── ImageDisplay.js
│   ├── App.js
│   └── index.js
├── package.json
└── README.md
```

### Key Technologies
- **React 18** - UI framework
- **Styled Components** - CSS-in-JS styling
- **MediaRecorder API** - Browser-based audio recording
- **Fetch API** - HTTP requests to backend

## API Integration

The frontend communicates with the Python backend via:
- `POST /api/process-voice` - Send audio file for processing
- `GET /api/health` - Health check endpoint

## Troubleshooting

### Microphone Access
If the recording doesn't work:
1. Check browser permissions for microphone access
2. Ensure you're using HTTPS (required for microphone access)
3. Try refreshing the page

### Backend Connection
If you get connection errors:
1. Ensure the Python backend is running on port 5000
2. Check that CORS is properly configured
3. Verify the proxy setting in package.json

## Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder. 