# ⚡ Quick Start Guide (5 Minutes)

Get DocuGenius running locally in 5 minutes!

---

## Prerequisites

✅ Python 3.11+ installed  
✅ Docker installed  
✅ Git installed

---

## Step 1: Clone & Install (1 min)

```bash
git clone https://github.com/yourusername/docugenius.git
cd docugenius

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 2: Supabase Account (2 min)

1. Go to [supabase.com](https://supabase.com) → **"New Project"**
2. Copy **Project URL** and **anon key**
3. Go to **SQL Editor** → Run `supabase_schema.sql`

---

## Step 3: Install Ollama (1 min)

**Windows:** Download from [ollama.ai/download](https://ollama.ai/download)

**Mac:**
```bash
brew install ollama && ollama serve &
```

**Linux:**
```bash
curl https://ollama.ai/install.sh | sh && ollama serve &
```

**Download model:**
```bash
ollama pull mistral
```

---

## Step 4: Start Meilisearch (30 sec)

```bash
docker-compose up -d
```

---

## Step 5: Configure (30 sec)

```bash
cp .env.example .env
```

Edit `.env`:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
MEILISEARCH_URL=http://localhost:7700
MEILISEARCH_MASTER_KEY=masterKey123
```

---

## Step 6: Run! (30 sec)

```bash
python -m uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000)

---

## 🎉 Done!

Upload a document and see the magic happen!

### Test Upload via CLI

```bash
curl -X POST http://localhost:8000/upload -F "file=@test.pdf"
```

### Test Search

```bash
curl "http://localhost:8000/search?q=your-query"
```

---

## ⚠️ Troubleshooting

**Ollama not working?**
```bash
ollama serve
# In another terminal:
ollama pull mistral
```

**Meilisearch not starting?**
```bash
docker-compose restart
```

**Module not found errors?**
```bash
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Next Steps

- Read [INSTALLATION.md](INSTALLATION.md) for detailed setup
- Read [README.md](README.md) for API docs
- Deploy to Render (see README.md)

---

**Total time:** ~5 minutes ⚡

