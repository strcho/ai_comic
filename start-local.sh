#!/bin/bash

# Start local development servers with pipenv

set -e

echo "🚀 Starting Comic Generation Agent (Local Development)..."
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please run ./setup-local.sh first, or copy .env.example to .env"
    exit 1
fi

# Check if backend .venv exists
if [ ! -d "backend/.venv" ]; then
    echo "❌ Backend virtual environment not found!"
    echo "Please run ./setup-local.sh first"
    exit 1
fi

# Check if frontend node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "❌ Frontend dependencies not installed!"
    echo "Please run ./setup-local.sh first"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping development servers..."
    if [ -n "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ -n "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    echo "✅ Development servers stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend
echo "📝 Starting backend server with pipenv..."
cd backend
pipenv run dev &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 3

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend server failed to start!"
    wait $BACKEND_PID
    exit 1
fi

echo "✅ Backend server started (PID: $BACKEND_PID)"

# Start frontend
echo "📝 Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Check if frontend started successfully
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "❌ Frontend server failed to start!"
    kill $BACKEND_PID 2>/dev/null || true
    wait $FRONTEND_PID
    exit 1
fi

echo "✅ Frontend server started (PID: $FRONTEND_PID)"

# Both servers are running
echo ""
echo "🎉 Comic Generation Agent is running!"
echo ""
echo "   Frontend:     http://localhost:5173"
echo "   Backend API:  http://localhost:8000"
echo "   API Docs:     http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID