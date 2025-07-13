#!/bin/bash

echo "========================================"
echo "Starting Eva's Coloring Sheet AI Frontend"
echo "========================================"
echo
echo "Starting React development server..."
echo "Frontend will be available at: http://localhost:3000"
echo
echo "Make sure the backend is running first!"
echo

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
    echo "ERROR: frontend directory not found!"
    echo "Please run setup_react_frontend.sh first."
    read -p "Press Enter to continue..."
    exit 1
fi

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "WARNING: React dependencies not installed!"
    echo "Installing dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Start the React development server
cd frontend
npm start 