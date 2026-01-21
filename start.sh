#!/bin/bash

echo "Starting Comic Generation Agent..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your OpenAI API key!"
    exit 1
fi

# Check if OPENAI_API_KEY is set
source .env
if [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ]; then
    echo "⚠️  Please set your OPENAI_API_KEY in the .env file!"
    exit 1
fi

# Create necessary directories
mkdir -p backend/output backend/cache backend/logs

# Build and start containers
docker-compose up --build -d

echo "✅ Comic Generation Agent is starting!"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "To stop the application: docker-compose down"
echo "To view logs: docker-compose logs -f"