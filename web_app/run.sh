#!/bin/bash

# Start GeoVision Campus Security Backend API

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  🎥 GeoVision Campus Security Backend API              ║"
echo "║     FastAPI Server                                     ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed"
    echo "Please install Python 3.10+ from https://www.python.org"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Seed database with sample data (optional)
if [ ! -f "gcs.db" ]; then
    echo "🌱 Seeding database with sample data..."
    python seed.py
fi

# Start the server
echo ""
echo "🚀 Starting FastAPI server on http://127.0.0.1:8000"
echo ""
echo "📚 API Documentation:"
echo "   - Swagger UI: http://127.0.0.1:8000/docs"
echo "   - ReDoc: http://127.0.0.1:8000/redoc"
echo "   - Health: http://127.0.0.1:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py
