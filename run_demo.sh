#!/bin/bash

# Tamatar-Bhai MVP Demo Script
# Automated setup and launch script

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored message
print_message() {
    echo -e "${2}${1}${NC}"
}

# Print header
print_header() {
    echo ""
    print_message "========================================" "$BLUE"
    print_message "$1" "$BLUE"
    print_message "========================================" "$BLUE"
    echo ""
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main script
main() {
    print_header "🍅 Tamatar-Bhai MVP Demo Setup"
    
    # Step 1: Check prerequisites
    print_message "Step 1: Checking prerequisites..." "$YELLOW"
    
    if ! command_exists docker; then
        print_message "❌ Docker is not installed. Please install Docker first." "$RED"
        exit 1
    fi
    print_message "✅ Docker found" "$GREEN"
    
    if ! command_exists docker-compose; then
        print_message "❌ Docker Compose is not installed. Please install Docker Compose first." "$RED"
        exit 1
    fi
    print_message "✅ Docker Compose found" "$GREEN"
    
    # Step 2: Check environment file
    print_message "\nStep 2: Checking environment configuration..." "$YELLOW"
    
    if [ ! -f .env ]; then
        print_message "⚠️  .env file not found. Creating from .env.example..." "$YELLOW"
        if [ -f .env.example ]; then
            cp .env.example .env
            print_message "✅ Created .env file" "$GREEN"
            print_message "⚠️  Please edit .env and add your API keys:" "$YELLOW"
            print_message "   - OPENAI_API_KEY" "$YELLOW"
            print_message "   - STABILITY_KEY" "$YELLOW"
            read -p "Press Enter after updating .env file..."
        else
            print_message "❌ .env.example not found" "$RED"
            exit 1
        fi
    else
        print_message "✅ .env file found" "$GREEN"
    fi
    
    # Check if API keys are set
    source .env
    if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_openai_key_here" ]; then
        print_message "⚠️  OPENAI_API_KEY not set in .env" "$YELLOW"
        print_message "   The application will use fallback responses" "$YELLOW"
    fi
    
    if [ -z "$STABILITY_KEY" ] || [ "$STABILITY_KEY" = "your_stability_key_here" ]; then
        print_message "⚠️  STABILITY_KEY not set in .env" "$YELLOW"
        print_message "   The application will use placeholder images" "$YELLOW"
    fi
    
    # Step 3: Stop any running containers
    print_message "\nStep 3: Cleaning up existing containers..." "$YELLOW"
    docker-compose down 2>/dev/null || true
    print_message "✅ Cleanup complete" "$GREEN"
    
    # Step 4: Build and start services
    print_header "🚀 Building and Starting Services"
    print_message "This may take a few minutes on first run..." "$YELLOW"
    
    docker-compose up --build -d
    
    # Step 5: Wait for services to be healthy
    print_message "\nStep 5: Waiting for services to be ready..." "$YELLOW"
    
    MAX_WAIT=60
    ELAPSED=0
    
    while [ $ELAPSED -lt $MAX_WAIT ]; do
        BACKEND_HEALTH=$(docker-compose ps | grep backend | grep -c "healthy" || echo "0")
        FRONTEND_HEALTH=$(docker-compose ps | grep frontend | grep -c "healthy" || echo "0")
        
        if [ "$BACKEND_HEALTH" = "1" ] && [ "$FRONTEND_HEALTH" = "1" ]; then
            print_message "✅ All services are healthy!" "$GREEN"
            break
        fi
        
        echo -n "."
        sleep 2
        ELAPSED=$((ELAPSED + 2))
    done
    
    if [ $ELAPSED -ge $MAX_WAIT ]; then
        print_message "\n⚠️  Services took longer than expected to start" "$YELLOW"
        print_message "   Check logs with: docker-compose logs" "$YELLOW"
    fi
    
    # Step 6: Display access information
    print_header "✅ Demo Ready!"
    
    print_message "🌐 Access the application:" "$GREEN"
    print_message "   Frontend:  http://localhost:3000" "$BLUE"
    print_message "   Backend:   http://localhost:8000" "$BLUE"
    print_message "   API Docs:  http://localhost:8000/docs" "$BLUE"
    
    print_message "\n📝 Quick Demo Flow:" "$GREEN"
    print_message "   1. Daily Preview: Try 'aloo paratha' for lunch" "$BLUE"
    print_message "   2. Switch-up Diff: Compare 'rajma' vs 'dal tadka'" "$BLUE"
    print_message "   3. Weekly Snapshot: View last 7 days" "$BLUE"
    
    print_message "\n🛑 To stop the demo:" "$GREEN"
    print_message "   docker-compose down" "$BLUE"
    
    print_message "\n📊 View logs:" "$GREEN"
    print_message "   docker-compose logs -f" "$BLUE"
    
    # Step 7: Open browser (optional)
    print_message "\n🌐 Opening browser..." "$YELLOW"
    
    if command_exists xdg-open; then
        xdg-open http://localhost:3000 2>/dev/null || true
    elif command_exists open; then
        open http://localhost:3000 2>/dev/null || true
    elif command_exists start; then
        start http://localhost:3000 2>/dev/null || true
    else
        print_message "⚠️  Could not open browser automatically" "$YELLOW"
        print_message "   Please open http://localhost:3000 manually" "$YELLOW"
    fi
    
    print_message "\n🎉 Demo is running! Enjoy!" "$GREEN"
    print_message "   Press Ctrl+C to view logs, or run 'docker-compose logs -f'" "$BLUE"
    
    # Follow logs
    docker-compose logs -f
}

# Run main function
main
