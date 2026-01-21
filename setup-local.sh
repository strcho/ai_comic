#!/bin/bash

# Local Development Setup Script
# This script helps set up development environment using pyenv

set -e

echo "🚀 Setting up Comic Generation Agent for local development..."
echo ""

# Check if pyenv is installed
if ! command -v pyenv &> /dev/null; then
    echo "❌ pyenv is not installed!"
    echo "Please install pyenv first:"
    echo "  macOS: brew install pyenv"
    echo "  Linux: Visit https://github.com/pyenv/pyenv#installation"
    echo ""
    echo "After installing pyenv, restart your terminal and run this script again."
    exit 1
fi

echo "✅ pyenv is installed: $(pyenv --version)"
echo ""

# Install Python 3.12 if not already installed
PYTHON_VERSION="3.12.0"
if ! pyenv versions | grep -q "$PYTHON_VERSION"; then
    echo "📦 Installing Python $PYTHON_VERSION..."
    echo "   This may take a few minutes..."
    pyenv install $PYTHON_VERSION
else
    echo "✅ Python $PYTHON_VERSION already installed"
fi

# Set local Python version
echo ""
echo "🔧 Setting Python $PYTHON_VERSION for this project..."
pyenv local $PYTHON_VERSION
echo "✅ Python version set to $(python --version)"
echo ""

# Setup backend
echo "📝 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Verify Python version in venv
echo "🔍 Python in venv: $(which python)"
echo "🔍 Python version: $(python --version)"

# Install dependencies
echo ""
echo "📦 Installing Python dependencies from requirements.txt..."
echo "   This may take a few minutes..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Python dependencies installed"

cd ..

# Setup frontend
echo ""
echo "📝 Setting up frontend..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
else
    echo "✅ Node.js dependencies already installed"
fi

# Create frontend .env file
if [ ! -f ".env" ]; then
    echo "📝 Creating frontend .env file..."
    echo "VITE_API_URL=http://localhost:8000" > .env
else
    echo "✅ Frontend .env file already exists"
fi

cd ..

# Setup .env file for backend
if [ ! -f ".env" ]; then
    echo ""
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your OPENAI_API_KEY!"
    echo ""
    read -p "Press Enter to continue after adding your API key..."
else
    echo "✅ .env file already exists"
fi

# Create output and cache directories
echo ""
echo "📁 Creating output directories..."
mkdir -p backend/output backend/cache backend/logs

# Done
echo ""
echo "✅ Local development environment setup complete!"
echo ""
echo "To start the development servers:"
echo ""
echo "1. Backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "2. Frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "Backend API:  http://localhost:8000"
echo "Frontend:     http://localhost:5173"
echo "API Docs:     http://localhost:8000/docs"
echo ""
echo "Happy coding! 🎨"