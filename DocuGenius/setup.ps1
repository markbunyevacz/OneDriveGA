# DocuGenius Setup Script for Windows
# Run this script in PowerShell to set up the application

Write-Host "🚀 DocuGenius Setup Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "📋 Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
    
    # Extract version number
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 11)) {
            Write-Host "❌ Python 3.11+ required. Please install from https://www.python.org/downloads/" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "❌ Python not found. Please install from https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "⚠️  Virtual environment already exists. Skipping..." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host ""
Write-Host "⬆️  Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install dependencies
Write-Host ""
Write-Host "📚 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Create .env file if it doesn't exist
Write-Host ""
Write-Host "⚙️  Checking configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "⚠️  .env file already exists. Skipping..." -ForegroundColor Yellow
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ Created .env file from template" -ForegroundColor Green
    Write-Host "⚠️  IMPORTANT: Edit .env file with your credentials!" -ForegroundColor Red
}

# Create uploads directory
Write-Host ""
Write-Host "📁 Creating uploads directory..." -ForegroundColor Yellow
if (Test-Path "uploads") {
    Write-Host "⚠️  Directory already exists. Skipping..." -ForegroundColor Yellow
} else {
    New-Item -ItemType Directory -Path "uploads" | Out-Null
    Write-Host "✓ Uploads directory created" -ForegroundColor Green
}

# Check Docker
Write-Host ""
Write-Host "🐳 Checking Docker..." -ForegroundColor Yellow
try {
    docker --version | Out-Null
    Write-Host "✓ Docker is installed" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Starting Meilisearch with Docker..." -ForegroundColor Yellow
    docker-compose up -d 2>&1 | Out-Null
    Write-Host "✓ Meilisearch started" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Docker not found. Please install Docker Desktop" -ForegroundColor Yellow
    Write-Host "   Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
}

# Check Ollama
Write-Host ""
Write-Host "🤖 Checking Ollama..." -ForegroundColor Yellow
try {
    $ollamaCheck = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing -ErrorAction SilentlyContinue
    Write-Host "✓ Ollama is running" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Ollama not running. Please install and start Ollama:" -ForegroundColor Yellow
    Write-Host "   1. Download from https://ollama.ai/download/windows" -ForegroundColor Yellow
    Write-Host "   2. Run: ollama pull mistral" -ForegroundColor Yellow
}

# Check Tesseract
Write-Host ""
Write-Host "📝 Checking Tesseract OCR..." -ForegroundColor Yellow
try {
    tesseract --version 2>&1 | Out-Null
    Write-Host "✓ Tesseract is installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Tesseract not found. Please install:" -ForegroundColor Yellow
    Write-Host "   Download from: https://github.com/UB-Mannheim/tesseract/wiki" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Edit .env file with your Supabase credentials" -ForegroundColor White
Write-Host "   2. Run SQL schema in Supabase: supabase_schema.sql" -ForegroundColor White
Write-Host "   3. Start the application:" -ForegroundColor White
Write-Host "      python -m uvicorn app.main:app --reload" -ForegroundColor Yellow
Write-Host ""
Write-Host "   4. Open browser: http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   - README.md - Full documentation" -ForegroundColor White
Write-Host "   - INSTALLATION.md - Detailed setup guide" -ForegroundColor White
Write-Host "   - QUICKSTART.md - 5-minute quick start" -ForegroundColor White
Write-Host ""
Write-Host "Need help? Check the troubleshooting section in README.md" -ForegroundColor Yellow
Write-Host ""

