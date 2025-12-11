# 📄 DocuGenius - Free AI-Powered Document Management

**Total Cost: $0/month** (completely free for 50-60 documents)

A complete document management system using 100% free and open-source tools:
- ✅ **Supabase PostgreSQL** (Free 500MB)
- ✅ **Ollama LLM** (Free, local AI)
- ✅ **Tesseract OCR** (Free, open-source)
- ✅ **Meilisearch** (Free, self-hosted)
- ✅ **FastAPI** (Free, Python)
- ✅ **Render.com** (Free deployment)

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites

- Python 3.11+
- Git
- Docker (for Meilisearch)

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/docugenius.git
cd docugenius
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Create Supabase Account (FREE)

1. Go to [supabase.com](https://supabase.com)
2. Click **"New Project"**
3. Copy your **Project URL** and **anon public key**
4. Go to **SQL Editor** and run `supabase_schema.sql`

### 3. Install Ollama (FREE)

**Windows:**
```bash
# Download from https://ollama.ai/download/windows
# Or use WSL:
curl https://ollama.ai/install.sh | sh
ollama pull mistral
```

**Mac:**
```bash
brew install ollama
ollama serve
ollama pull mistral
```

**Linux:**
```bash
curl https://ollama.ai/install.sh | sh
ollama serve
ollama pull mistral
```

### 4. Install Tesseract OCR (FREE)

**Windows:**
```bash
# Download installer from:
# https://github.com/UB-Mannheim/tesseract/wiki

# Add to PATH or set in .env:
# TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

**Mac:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### 5. Run Meilisearch (FREE)

```bash
# Start with Docker Compose
docker-compose up -d

# Or run directly:
docker run -p 7700:7700 -v meilisearch_data:/meili_data getmeili/meilisearch
```

### 6. Configure Environment

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Supabase (from step 2)
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_KEY=your-anon-key-here

# Ollama (default if running locally)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Meilisearch (default if using docker-compose)
MEILISEARCH_URL=http://localhost:7700
MEILISEARCH_MASTER_KEY=masterKey123

# Tesseract (only if not in PATH)
TESSERACT_CMD=tesseract
```

### 7. Run Locally

```bash
# Start the application
python -m uvicorn app.main:app --reload

# Or
python app/main.py
```

Visit: **http://localhost:8000**

---

## 🧪 Test the System

### 1. Upload a Document

Open the web interface and upload a PDF, DOCX, or image file.

### 2. Test via API

```bash
# Upload document
curl -X POST http://localhost:8000/upload \
  -F "file=@test_document.pdf"

# Search documents
curl "http://localhost:8000/search?q=marketing&country=HU"

# List all documents
curl http://localhost:8000/documents

# Health check
curl http://localhost:8000/health
```

---

## ☁️ Deploy to Render (FREE)

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/docugenius.git
git push -u origin main
```

### 2. Deploy on Render

1. Go to [render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo
4. Render auto-detects settings from `render.yaml`
5. Add environment variables:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `MEILISEARCH_URL` (external service)
   - `MEILISEARCH_MASTER_KEY`

6. Click **"Create Web Service"**

**Note:** Ollama won't run on Render free tier. The app will use rule-based classification as fallback.

### 3. Deploy Meilisearch Separately

**Option A: Run on VPS ($5/month)**
```bash
# DigitalOcean, Hetzner, Linode, etc.
docker run -d -p 7700:7700 \
  -v /var/lib/meilisearch:/meili_data \
  -e MEILI_MASTER_KEY=your-secure-key \
  getmeili/meilisearch
```

**Option B: Meilisearch Cloud (Free Trial)**
```bash
# Sign up at https://www.meilisearch.com/cloud
# Get your URL and API key
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────┐
│         USER (Browser / API)                │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│      FastAPI Backend (Render.com FREE)      │
│  • Upload handling                          │
│  • REST API                                 │
│  • Orchestration                            │
└─────────────────────────────────────────────┘
         ↓              ↓              ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Tesseract   │ │    Ollama    │ │  Meilisearch │
│     OCR      │ │   (Local)    │ │   (Docker)   │
│    (Free)    │ │   Mistral    │ │    (Free)    │
└──────────────┘ └──────────────┘ └──────────────┘
                         ↓
                ┌──────────────────┐
                │    Supabase      │
                │   PostgreSQL     │
                │   (Free 500MB)   │
                └──────────────────┘
```

---

## 🔧 API Documentation

### Endpoints

#### `POST /upload`
Upload and process a document.

**Request:**
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "filename": "document.pdf",
  "file_type": "pdf",
  "file_size": 1024000,
  "content": "Extracted text...",
  "classification": {
    "country": ["HU", "USA"],
    "technology": ["AI", "Cloud"],
    "product": ["ProductA"],
    "document_type": "marketing",
    "confidence": 0.85
  },
  "status": "processed",
  "created_at": "2025-12-11T10:00:00Z"
}
```

#### `GET /search`
Search documents with filters.

**Parameters:**
- `q` (required): Search query
- `country` (optional): Filter by country
- `technology` (optional): Filter by technology
- `document_type` (optional): Filter by type
- `limit` (optional): Max results (default: 10)

**Example:**
```bash
curl "http://localhost:8000/search?q=AI&country=HU&limit=5"
```

#### `GET /documents`
List all documents with pagination.

**Parameters:**
- `limit` (optional): Max results (default: 10)
- `offset` (optional): Skip N documents (default: 0)

#### `GET /documents/{doc_id}`
Get a specific document.

#### `DELETE /documents/{doc_id}`
Delete a document.

#### `GET /health`
Health check endpoint.

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

## 💰 Cost Breakdown

| Component | Cost | Details |
|-----------|------|---------|
| **Supabase** | $0 | 500MB storage, unlimited API requests |
| **Ollama** | $0 | Local LLM, runs on your machine |
| **Tesseract** | $0 | Open-source OCR |
| **Meilisearch** | $0 | Self-hosted in Docker |
| **FastAPI** | $0 | Python framework |
| **Render.com** | $0 | Free tier (750 hours/month) |
| **GitHub** | $0 | Free public/private repos |
| **TOTAL** | **$0** | Completely free! |

### Optional Upgrades

If you need better performance:

| Upgrade | Cost | Benefit |
|---------|------|---------|
| Render Paid Tier | $7/month | No cold starts, better performance |
| VPS for Meilisearch | $5/month | Faster search, more storage |
| Cloud LLM API | Pay-per-use | Better classification accuracy |

**Total with upgrades:** ~$12/month (still 10x cheaper than Azure)

---

## 🔥 Features

### ✅ Implemented

- [x] Document upload (PDF, DOCX, images, text)
- [x] OCR text extraction (Tesseract)
- [x] AI classification (Ollama Mistral)
- [x] Full-text search (Meilisearch)
- [x] PostgreSQL storage (Supabase)
- [x] REST API (FastAPI)
- [x] Beautiful web UI
- [x] Health monitoring
- [x] Rule-based fallback (when Ollama unavailable)

### 🚧 Coming Soon

- [ ] OneDrive integration
- [ ] Batch processing
- [ ] Advanced filters
- [ ] Export to Excel/CSV
- [ ] User authentication
- [ ] Multi-language OCR
- [ ] Email notifications

---

## 🐛 Troubleshooting

### Ollama Not Working

**Symptom:** Classification confidence is always 0.6

**Solution:**
```bash
# Check if Ollama is running
ollama list

# Start Ollama
ollama serve

# Pull model if missing
ollama pull mistral

# Test manually
curl http://localhost:11434/api/tags
```

### Tesseract Not Found

**Windows:**
```bash
# Set full path in .env
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

**Mac/Linux:**
```bash
which tesseract
# Add to .env if not in PATH
```

### Meilisearch Connection Error

```bash
# Check if running
docker ps

# Restart
docker-compose restart meilisearch

# Check logs
docker logs docugenius-meilisearch
```

### Supabase Connection Error

1. Check `.env` credentials
2. Verify project is active in Supabase dashboard
3. Check if SQL schema was executed
4. Test connection:
```bash
curl https://YOUR_PROJECT.supabase.co/rest/v1/ \
  -H "apikey: YOUR_KEY"
```

---

## 🧑‍💻 Development

### Project Structure

```
docugenius/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── document.py      # Data models
│   └── services/
│       ├── __init__.py
│       ├── database.py      # Supabase integration
│       ├── document_processor.py  # OCR + AI
│       └── search.py        # Meilisearch
├── uploads/                 # Uploaded files (gitignored)
├── requirements.txt
├── .env.example
├── .env                     # Your config (gitignored)
├── docker-compose.yml
├── render.yaml
├── supabase_schema.sql
└── README.md
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# With coverage
pytest --cov=app
```

### Adding New Document Types

Edit `app/services/document_processor.py`:

```python
async def _extract_text(self, content: bytes, file_type: str) -> str:
    if file_type == "your_type":
        return await self._extract_from_your_type(content)
```

---

## 📚 Resources

- **FastAPI:** https://fastapi.tiangolo.com/
- **Supabase:** https://supabase.com/docs
- **Ollama:** https://ollama.ai/
- **Tesseract:** https://github.com/tesseract-ocr/tesseract
- **Meilisearch:** https://docs.meilisearch.com/
- **Render:** https://render.com/docs

---

## 📄 License

MIT License - Use freely!

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📞 Support

- **Issues:** https://github.com/yourusername/docugenius/issues
- **Discussions:** https://github.com/yourusername/docugenius/discussions

---

## ⭐ Star History

If you find this useful, please star the repo!

---

**Built with ❤️ using 100% free and open-source tools**

No vendor lock-in • Privacy-first • Scalable • Production-ready

