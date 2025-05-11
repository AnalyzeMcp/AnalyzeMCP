#!/bin/bash

# Build script for AnalyzeMCP project

echo "Starting AnalyzeMCP build process..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Build frontend
echo "Building frontend..."
cd src/frontend
npm install
npm run build
cd ../..

# Run tests
echo "Running tests..."
python -m pytest tests/

echo "Build process completed successfully!"