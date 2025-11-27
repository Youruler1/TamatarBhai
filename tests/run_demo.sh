#!/bin/bash

# Tamatar-Bhai MVP Demo Script
echo "🍅 Starting Tamatar-Bhai MVP Demo..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Please copy .env.example to .env and add your API keys."
    echo "   Required: OPENAI_API_KEY and STABILITY_KEY"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Create data directory if it doesn't exist
mkdir -p data/images

echo "🐳 Building and starting containers..."
docker-compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running at http://localhost:8000"
else
    echo "⚠️  Backend may still be starting..."
fi

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is running at http://localhost:3000"
else
    echo "⚠️  Frontend may still be starting..."
fi

echo ""
echo "🎉 Tamatar-Bhai MVP is ready!"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Demo Flow:"
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Try Daily Preview with 'aloo paratha' and 'lunch'"
echo "   3. Test Switch-up Diff with 'rajma' vs 'dal'"
echo "   4. Check Weekly Snapshot with date range"
echo ""
echo "🛑 To stop: docker-compose down"
echo "📊 To view logs: docker-compose logs -f"