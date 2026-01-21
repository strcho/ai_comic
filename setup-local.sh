#!/bin/bash

# Local Development Setup Script with pipenv
# This script helps set up development environment using pipenv

set -e

echo "🚀 Setting up Comic Generation Agent for local development..."
echo ""

# Check if pipenv is installed
if ! command -v pipenv &> /dev/null; then
    echo "❌ pipenv is not installed!"
    echo "Please install pipenv first:"
    echo "  pip install pipenv"
    echo "  or"
    echo "  brew install pipenv"
    echo ""
    echo "After installing pipenv, restart your terminal and run this script again."
    exit 1
fi

echo "✅ pipenv is installed: $(pipenv --version)"
echo ""

# Check Python version
echo "🔍 Checking Python version..."
python3 --version
echo ""

# Setup backend
echo "📝 Setting up backend..."
cd backend

# Create .venv directory
echo "🔧 Creating virtual environment with pipenv..."
# Skip if venv already exists
if [ ! -d ".venv" ]; then
    pipenv install --dev
else
    echo "✅ Virtual environment already exists"
    pipenv install --dev
fi

echo "✅ Backend dependencies installed"
echo ""

cd ..

# Setup frontend
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
echo "To start development servers:"
echo ""
echo "1. Backend (Terminal 1):"
echo "   cd backend"
echo "   pipenv run dev"
echo "   # or:"
echo "   pipenv shell"
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