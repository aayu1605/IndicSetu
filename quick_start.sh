#!/bin/bash

# Indic-Setu Quick Start Script
# Usage: bash quick_start.sh

echo "🌾 Indic-Setu - Quick Start Script"
echo "===================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "📦 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"
echo ""

# Create virtual environment
echo "📁 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✅ Pip upgraded${NC}"
echo ""

# Install requirements
echo "📥 Installing dependencies..."
pip install streamlit requests pyttsx3 python-dotenv > /dev/null 2>&1
echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

# Check for app.py
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ app.py not found in current directory${NC}"
    echo "Please ensure app.py is in the same directory as this script"
    exit 1
fi

echo "🚀 Starting Indic-Setu Streamlit App..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  App will open at: http://localhost:8501"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}📋 First Time Setup:${NC}"
echo "1. Paste your AWS API Gateway URL in Settings (Sidebar)"
echo "2. Select your Occupation and Income"
echo "3. Ask a question about government schemes"
echo "4. Check the response!"
echo ""

# Run Streamlit
streamlit run app.py

echo ""
echo -e "${GREEN}✅ Thanks for using Indic-Setu!${NC}"
