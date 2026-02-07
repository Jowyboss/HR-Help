#!/bin/bash

# HR Help Desk - Quick Start Script
# This script sets up and runs the HR Help Desk application with SQLite

set -e  # Exit on error

echo "🎫 HR Help Desk - Quick Start Setup"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Error: Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_CMD=$(command -v python3 || command -v python)
echo "✓ Found Python: $PYTHON_CMD"

# Navigate to script directory
cd "$(dirname "$0")"

# Step 1: Install dependencies if needed
echo ""
echo "📦 Step 1: Installing Python dependencies..."
cd backend
$PYTHON_CMD -m pip install -r requirements.txt -q
cd ..

# Step 2: Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "⚙️  Step 2: Creating .env configuration..."
    cat > .env << 'EOF'
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_TYPE=sqlite
DATABASE_NAME=hr_helpdesk
FLASK_ENV=development
EOF
    echo "✓ Created .env file"
else
    echo ""
    echo "✓ Using existing .env file"
fi

# Step 3: Set up database with sample data
echo ""
echo "🗄️  Step 3: Setting up database with sample data..."
cd backend
$PYTHON_CMD populate_db.py
cd ..

# Step 4: Instructions for running
echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application, run these commands in separate terminal windows:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend && python app.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend && python -m http.server 8080"
echo ""
echo "Then open your browser to:"
echo "  📝 Submit Ticket: http://localhost:8080/index.html"
echo "  📊 Dashboard:     http://localhost:8080/dashboard.html"
echo ""
echo "Would you like to start the servers now? (Ctrl+C to cancel)"
read -p "Press Enter to start..."

# Start backend in background
echo ""
echo "🚀 Starting backend server..."
cd backend
$PYTHON_CMD app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend server
echo "🚀 Starting frontend server..."
cd frontend
$PYTHON_CMD -m http.server 8080 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 2

echo ""
echo "✅ Servers are running!"
echo ""
echo "  📝 Submit Ticket: http://localhost:8080/index.html"
echo "  📊 Dashboard:     http://localhost:8080/dashboard.html"
echo "  🔧 API:           http://localhost:5000/api/tickets"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo "✓ Servers stopped"
    exit 0
}

# Set up trap for cleanup
trap cleanup INT TERM

# Wait for user interrupt
wait
