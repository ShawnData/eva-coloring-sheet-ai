#!/bin/bash

echo "========================================"
echo "Starting Eva's Coloring Sheet AI Backend"
echo "========================================"
echo
echo "Starting Python API server..."
echo "Backend will be available at: http://localhost:5000"
echo
echo "Press Ctrl+C to stop the server"
echo

# Check if .env file exists
if [ ! -f .env ]; then
    echo "WARNING: .env file not found!"
    echo "Please create a .env file with your OpenAI API key:"
    echo "OPENAI_API_KEY=your_api_key_here"
    echo
    read -p "Press Enter to continue anyway..."
fi

# Start the FastAPI server with Uvicorn
uvicorn api_server:app --host 0.0.0.0 --port 5000 --reload 