#!/bin/bash
# DocuGenius Setup Script for Mac/Linux
# Run this script to set up the application

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🚀 DocuGenius Setup Script${NC}"
echo -e "${CYAN}================================${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}📋 Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo -e "${GREEN}✓ Found: Python $PYTHON_VERSION${NC}"
    
    # Check if version is 3.11+
    MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 11 ]); then
        echo -e "${RED}❌ Python 3.11+ required. Please upgrade Python.${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Python not found. Please install Python 3.11+${NC}"
    exit 1
fi

# Create virtual environment
echo ""
echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists. Skipping...${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo ""
echo -e "${YELLOW}🔌 Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo ""
echo -e "${YELLOW}⬆️  Upgrading pip...${NC}"
pip install --upgrade pip --quiet

# Install dependencies
echo ""
echo -e "${YELLOW}📚 Installing dependencies...${NC}"
pip install -r requirements.txt --quiet
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Create .env file
echo ""
echo -e "${YELLOW}⚙️  Checking configuration...${NC}"
if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file already exists. Skipping...${NC}"
else
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file from template${NC}"
    echo -e "${RED}⚠️  IMPORTANT: Edit .env file with your credentials!${NC}"
fi

# Create uploads directory
echo ""
echo -e "${YELLOW}📁 Creating uploads directory...${NC}"
if [ -d "uploads" ]; then
    echo -e "${YELLOW}⚠️  Directory already exists. Skipping...${NC}"
else
    mkdir uploads
    echo -e "${GREEN}✓ Uploads directory created${NC}"
fi

# Check Docker
echo ""
echo -e "${YELLOW}🐳 Checking Docker...${NC}"
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓ Docker is installed${NC}"
    
    echo ""
    echo -e "${YELLOW}Starting Meilisearch with Docker...${NC}"
    docker-compose up -d > /dev/null 2>&1 || true
    echo -e "${GREEN}✓ Meilisearch started${NC}"
else
    echo -e "${YELLOW}⚠️  Docker not found. Please install Docker:${NC}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "   brew install --cask docker"
    else
        echo "   curl -fsSL https://get.docker.com | sh"
    fi
fi

# Check Ollama
echo ""
echo -e "${YELLOW}🤖 Checking Ollama...${NC}"
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✓ Ollama is installed${NC}"
    
    # Check if Ollama is running
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Ollama is running${NC}"
    else
        echo -e "${YELLOW}⚠️  Starting Ollama...${NC}"
        ollama serve > /dev/null 2>&1 &
        sleep 2
        echo -e "${GREEN}✓ Ollama started${NC}"
    fi
    
    # Check if model is downloaded
    if ollama list | grep -q "mistral"; then
        echo -e "${GREEN}✓ Mistral model is installed${NC}"
    else
        echo -e "${YELLOW}⚠️  Downloading Mistral model (this may take a few minutes)...${NC}"
        ollama pull mistral
        echo -e "${GREEN}✓ Mistral model downloaded${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Ollama not found. Please install:${NC}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "   brew install ollama"
    else
        echo "   curl https://ollama.ai/install.sh | sh"
    fi
fi

# Check Tesseract
echo ""
echo -e "${YELLOW}📝 Checking Tesseract OCR...${NC}"
if command -v tesseract &> /dev/null; then
    TESSERACT_VERSION=$(tesseract --version 2>&1 | head -n1)
    echo -e "${GREEN}✓ $TESSERACT_VERSION${NC}"
else
    echo -e "${YELLOW}⚠️  Tesseract not found. Please install:${NC}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "   brew install tesseract"
    else
        echo "   sudo apt-get install tesseract-ocr"
    fi
fi

# Summary
echo ""
echo -e "${CYAN}================================${NC}"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "${CYAN}================================${NC}"
echo ""
echo -e "${CYAN}📋 Next Steps:${NC}"
echo -e "   1. Edit .env file with your Supabase credentials"
echo -e "   2. Run SQL schema in Supabase: supabase_schema.sql"
echo -e "   3. Start the application:"
echo -e "      ${YELLOW}source venv/bin/activate${NC}"
echo -e "      ${YELLOW}python -m uvicorn app.main:app --reload${NC}"
echo ""
echo -e "   4. Open browser: ${YELLOW}http://localhost:8000${NC}"
echo ""
echo -e "${CYAN}📚 Documentation:${NC}"
echo -e "   - README.md - Full documentation"
echo -e "   - INSTALLATION.md - Detailed setup guide"
echo -e "   - QUICKSTART.md - 5-minute quick start"
echo ""
echo -e "${YELLOW}Need help? Check the troubleshooting section in README.md${NC}"
echo ""

