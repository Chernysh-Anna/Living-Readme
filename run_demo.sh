#!/bin/bash
# Living README Agent - Quick Demo Script

set -e

echo "🤖 Living README Agent - Quick Demo"
echo "===================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo "✓ Node.js found: $(node --version)"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -q -r agent/requirements.txt
echo "✓ Python dependencies installed"
echo ""

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd target-app
npm install --silent
cd ..
echo "✓ Node.js dependencies installed"
echo ""

# Run the agent
echo "🚀 Running Living README Agent..."
echo ""
cd agent
python main.py
cd ..

echo ""
echo "===================================="
echo "✅ Demo Complete!"
echo ""
echo "📊 Check the reports in bob_sessions/"
echo "📝 Review the updated target-app/README.md"
echo "📖 See DEMO.md for more scenarios"
echo ""

# Made with Bob
