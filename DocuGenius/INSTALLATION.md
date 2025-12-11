# 🛠️ Complete Installation Guide

Step-by-step instructions for setting up DocuGenius from scratch.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Python Environment](#step-1-python-environment)
3. [Step 2: Supabase Setup](#step-2-supabase-setup)
4. [Step 3: Ollama Installation](#step-3-ollama-installation)
5. [Step 4: Tesseract OCR Installation](#step-4-tesseract-ocr-installation)
6. [Step 5: Meilisearch Setup](#step-5-meilisearch-setup)
7. [Step 6: Application Configuration](#step-6-application-configuration)
8. [Step 7: First Run](#step-7-first-run)
9. [Step 8: Deployment (Optional)](#step-8-deployment-optional)

---

## Prerequisites

- **Operating System:** Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python:** 3.11 or higher
- **RAM:** Minimum 4GB (8GB recommended for Ollama)
- **Disk Space:** 10GB free (for Ollama models)
- **Internet:** Required for initial setup

---

## Step 1: Python Environment

### Windows

```powershell
# Check Python version
python --version

# Should show Python 3.11.x or higher
# If not, download from https://www.python.org/downloads/

# Clone repository
git clone https://github.com/yourusername/docugenius.git
cd docugenius

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### macOS / Linux

```bash
# Check Python version
python3 --version

# Clone repository
git clone https://github.com/yourusername/docugenius.git
cd docugenius

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

---

## Step 2: Supabase Setup

### 2.1 Create Account

1. Go to [https://supabase.com](https://supabase.com)
2. Click **"Start your project"**
3. Sign up with GitHub, Google, or email
4. Verify your email

### 2.2 Create Project

1. Click **"New Project"**
2. Fill in details:
   - **Name:** `docugenius` (or your choice)
   - **Database Password:** Generate a strong password (save it!)
   - **Region:** Choose closest to you
   - **Pricing Plan:** Free
3. Click **"Create new project"**
4. Wait 2-3 minutes for setup

### 2.3 Get API Credentials

1. Go to **Settings** → **API**
2. Copy these values:
   - **Project URL:** `https://xxxxxxxxxxxx.supabase.co`
   - **anon public key:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
3. Save them for later

### 2.4 Create Database Table

1. Go to **SQL Editor** in left menu
2. Click **"New Query"**
3. Copy and paste contents of `supabase_schema.sql`
4. Click **"Run"** (or press F5)
5. You should see: "Success. No rows returned"

### 2.5 Verify Table Creation

1. Go to **Table Editor** in left menu
2. You should see `documents` table
3. Check columns: id, filename, file_type, content, etc.

---

## Step 3: Ollama Installation

Ollama provides free local LLM inference.

### Windows

**Option A: Native Windows (Recommended)**

1. Download installer from [https://ollama.ai/download/windows](https://ollama.ai/download/windows)
2. Run `OllamaSetup.exe`
3. Follow installation wizard
4. Ollama starts automatically

**Option B: WSL2**

```bash
# Open WSL2 terminal
curl https://ollama.ai/install.sh | sh

# Start Ollama server
ollama serve &
```

### macOS

```bash
# Install with Homebrew
brew install ollama

# Or download from https://ollama.ai/download/mac

# Start Ollama
ollama serve
```

### Linux

```bash
# Install
curl https://ollama.ai/install.sh | sh

# Start as service
sudo systemctl start ollama
sudo systemctl enable ollama

# Or run manually
ollama serve
```

### Download Model

```bash
# Download Mistral 7B model (~4GB)
ollama pull mistral

# Wait for download to complete
# This may take 5-10 minutes depending on internet speed

# Verify installation
ollama list
# Should show: mistral:latest

# Test the model
ollama run mistral "Hello, how are you?"
```

### Troubleshooting Ollama

**Check if running:**
```bash
curl http://localhost:11434/api/tags
# Should return JSON with available models
```

**Restart Ollama:**
```bash
# Windows: Restart from system tray
# macOS/Linux:
pkill ollama
ollama serve
```

---

## Step 4: Tesseract OCR Installation

### Windows

1. Download installer from:
   [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

2. Run installer `tesseract-ocr-w64-setup-5.3.3.exe`

3. **Important:** Check "Add to PATH" during installation

4. Default install path: `C:\Program Files\Tesseract-OCR\`

5. Verify installation:
```powershell
tesseract --version
# Should show: tesseract 5.3.3
```

6. If not in PATH, note the full path for `.env` configuration

### macOS

```bash
# Install with Homebrew
brew install tesseract

# Verify
tesseract --version
```

### Linux (Ubuntu/Debian)

```bash
# Install
sudo apt-get update
sudo apt-get install tesseract-ocr

# Verify
tesseract --version
```

### Linux (RHEL/CentOS/Fedora)

```bash
# Install
sudo yum install tesseract

# Verify
tesseract --version
```

### Additional Languages (Optional)

```bash
# Windows: Download language packs from Tesseract wiki
# macOS:
brew install tesseract-lang

# Linux:
sudo apt-get install tesseract-ocr-eng  # English
sudo apt-get install tesseract-ocr-hun  # Hungarian
sudo apt-get install tesseract-ocr-deu  # German
```

---

## Step 5: Meilisearch Setup

### Option A: Docker (Recommended)

**Install Docker:**
- Windows: [Docker Desktop](https://www.docker.com/products/docker-desktop)
- macOS: `brew install --cask docker`
- Linux: `sudo apt-get install docker.io docker-compose`

**Run Meilisearch:**

```bash
# Using docker-compose (easiest)
docker-compose up -d

# Verify running
docker ps
# Should show: docugenius-meilisearch

# Check logs
docker logs docugenius-meilisearch
```

### Option B: Direct Docker Run

```bash
docker run -d -p 7700:7700 \
  --name docugenius-meilisearch \
  -e MEILI_ENV=development \
  -e MEILI_MASTER_KEY=masterKey123 \
  -v meilisearch_data:/meili_data \
  getmeili/meilisearch:v1.5

# Verify
curl http://localhost:7700/health
# Should return: {"status":"available"}
```

### Option C: Native Installation

**macOS:**
```bash
brew install meilisearch
meilisearch --env development
```

**Linux:**
```bash
# Download binary
curl -L https://install.meilisearch.com | sh

# Run
./meilisearch --env development
```

**Windows:**
```powershell
# Download from https://github.com/meilisearch/meilisearch/releases
# Extract and run
.\meilisearch.exe --env development
```

---

## Step 6: Application Configuration

### 6.1 Create Environment File

```bash
# Copy example file
cp .env.example .env

# Or on Windows:
copy .env.example .env
```

### 6.2 Edit Configuration

Open `.env` in your favorite editor and fill in values:

```env
# Supabase (from Step 2.3)
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Ollama (default if running locally)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Meilisearch (default from docker-compose)
MEILISEARCH_URL=http://localhost:7700
MEILISEARCH_MASTER_KEY=masterKey123

# Application
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Tesseract (only set if NOT in PATH)
# Windows example:
# TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
TESSERACT_CMD=tesseract
```

### 6.3 Create Upload Directory

```bash
mkdir uploads
```

---

## Step 7: First Run

### 7.1 Start All Services

**Terminal 1: Meilisearch** (if not using Docker)
```bash
docker-compose up
```

**Terminal 2: Ollama** (if not already running)
```bash
ollama serve
```

**Terminal 3: Application**
```bash
# Activate virtual environment first!
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Run application
python -m uvicorn app.main:app --reload

# Or simply:
python app/main.py
```

### 7.2 Verify Startup

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Starting DocuGenius v1.0.0
INFO:     ✓ Database initialized
INFO:     ✓ Search index initialized
INFO:     ✓ Ollama connected
```

### 7.3 Open Browser

Navigate to: [http://localhost:8000](http://localhost:8000)

You should see the DocuGenius homepage!

### 7.4 First Upload Test

1. Click **"Choose File"**
2. Select a PDF, DOCX, or image file
3. Click **"🚀 Upload & Process"**
4. Wait for processing (5-30 seconds)
5. See results with AI classification!

### 7.5 API Health Check

```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "app": "DocuGenius",
  "version": "1.0.0",
  "services": {
    "database": true,
    "search": true,
    "ollama": true
  }
}
```

---

## Step 8: Deployment (Optional)

### Deploy to Render.com (FREE)

#### 8.1 Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/docugenius.git
git push -u origin main
```

#### 8.2 Create Render Account

1. Go to [https://render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your repos

#### 8.3 Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Select your `docugenius` repository
3. Render auto-detects settings from `render.yaml`
4. Add environment variables:
   - `SUPABASE_URL`: Your Supabase URL
   - `SUPABASE_KEY`: Your Supabase key
   - `MEILISEARCH_URL`: External Meilisearch URL
   - `MEILISEARCH_MASTER_KEY`: Your master key

5. Click **"Create Web Service"**
6. Wait 5-10 minutes for deployment

#### 8.4 Deploy Meilisearch

**Option A: VPS (DigitalOcean, Hetzner, Linode)**

```bash
# SSH into your VPS
ssh user@your-vps-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Run Meilisearch
docker run -d -p 7700:7700 \
  --name meilisearch \
  -e MEILI_MASTER_KEY=your-secure-random-key \
  -v /var/lib/meilisearch:/meili_data \
  --restart unless-stopped \
  getmeili/meilisearch:v1.5

# Configure firewall
ufw allow 7700/tcp
```

**Option B: Meilisearch Cloud**

1. Sign up at [https://www.meilisearch.com/cloud](https://www.meilisearch.com/cloud)
2. Create a new instance
3. Copy URL and API key
4. Add to Render environment variables

#### 8.5 Access Deployed App

Your app will be available at:
`https://docugenius-api.onrender.com`

**Note:** Free tier has cold starts (~10-30 seconds for first request after inactivity)

---

## 🎉 Installation Complete!

You now have a fully functional document management system!

### What's Next?

- Upload more documents to test
- Try the search API
- Customize classification prompts
- Add more document types
- Integrate with OneDrive (see BLOKK_AI_Workflow_Guide.md)

### Need Help?

- Check [README.md](README.md) for troubleshooting
- Review [API documentation](README.md#api-documentation)
- Open an issue on GitHub

---

## ⏱️ Installation Time Estimate

| Step | Time |
|------|------|
| Python environment | 5 min |
| Supabase setup | 10 min |
| Ollama installation | 15 min (including model download) |
| Tesseract installation | 5 min |
| Meilisearch setup | 5 min |
| Configuration | 5 min |
| **Total** | **~45 min** |

---

**Happy Document Managing! 🚀**

