#!/bin/bash

echo "========================================"
echo "Eva's Coloring Sheet AI - React Setup"
echo "========================================"
echo

echo "Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed!"
    echo
    echo "Please install Node.js from https://nodejs.org/"
    echo "Download the LTS version and run the installer."
    echo
    echo "After installation, close this terminal and run this script again."
    read -p "Press Enter to continue..."
    exit 1
fi

echo "Node.js is installed! Version: $(node --version)"
echo "npm version: $(npm --version)"
echo

echo "Installing React frontend dependencies..."
cd frontend
if ! npm install; then
    echo "ERROR: Failed to install dependencies!"
    read -p "Press Enter to continue..."
    exit 1
fi

echo
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo
echo "To start the application:"
echo
echo "1. Start the Python backend (in a new terminal):"
echo "   ./start_backend.sh"
echo "   or"
echo "   uvicorn api_server:app --host 0.0.0.0 --port 5000 --reload"
echo
echo "2. Start the React frontend (in another terminal):"
echo "   ./start_frontend.sh"
echo "   or"
echo "   cd frontend && npm start"
echo
echo "3. Open your browser to: http://localhost:3000"
echo
read -p "Press Enter to continue..." 