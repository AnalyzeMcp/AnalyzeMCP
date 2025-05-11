#!/bin/bash

# Deployment script for AnalyzeMCP project

echo "Starting AnalyzeMCP deployment..."

# Configuration
APP_NAME="AnalyzeMCP"
APP_PORT=8000

# Activate virtual environment
source venv/bin/activate

# Check if port is in use
if lsof -Pi :$APP_PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "Port $APP_PORT is already in use. Stopping existing process..."
    lsof -ti :$APP_PORT | xargs kill -9
fi

# Start backend service
echo "Starting backend service..."
python -m src.api.routes &

# Start frontend development server
echo "Starting frontend server..."
cd src/frontend
npm run dev &

echo "Deployment completed!"
echo "Backend API is running on http://localhost:$APP_PORT"
echo "Frontend is running on http://localhost:5173"