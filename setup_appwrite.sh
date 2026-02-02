#!/bin/bash
# Setup script for PotatoMail Appwrite collections
# This script validates the environment and runs the Python setup script

set -e

echo "=================================="
echo "PotatoMail Appwrite Setup"
echo "=================================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "❌ Error: .env file not found"
    echo ""
    echo "Please copy .env.example to .env and fill in your Appwrite credentials:"
    echo "  cp .env.example .env"
    echo ""
    exit 1
fi

# Check if Python dependencies are installed
echo ""
echo "📦 Checking dependencies..."
if ! python3 -c "import appwrite" 2>/dev/null; then
    echo "⚠️  Appwrite SDK not found. Installing dependencies..."
    uv sync
fi

# Run the setup script
echo ""
echo "🚀 Running Appwrite collections setup..."
uv run python setup_appwrite.py
