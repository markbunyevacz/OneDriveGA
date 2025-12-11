# 🚀 Deployment Guide

Complete guide for deploying DocuGenius to production.

---

## Deployment Options

1. **Render.com (Free)** - Recommended for small projects
2. **Railway.app (Free)** - Alternative to Render
3. **Heroku** - Pay-per-use
4. **VPS (DigitalOcean, Hetzner)** - Full control
5. **Docker Container** - Any cloud provider

---

## Option 1: Render.com (FREE)

### Cost: $0/month
- Free tier: 750 hours/month
- Cold starts after 15 minutes of inactivity
- Automatic HTTPS
- GitHub integration

### Step-by-Step

#### 1. Prepare Repository

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/docugenius.git
git push -u origin main
```

#### 2. Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access repositories

#### 3. Deploy Application

1. Click **"New +"** → **"Web Service"**
2. Select your repository
3. Configuration (auto-detected from `render.yaml`):
   - **Name:** docugenius-api
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### 4. Add Environment Variables

In Render dashboard, add:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
MEILISEARCH_URL=https://your-meilisearch-url.com
MEILISEARCH_MASTER_KEY=your-master-key
DEBUG=False
MAX_UPLOAD_SIZE=10485760
```

#### 5. Deploy

Click **"Create Web Service"** and wait 5-10 minutes.

Your app will be live at: `https://docugenius-api.onrender.com`

### Important Notes

⚠️ **Ollama won't work on Render free tier** (requires GPU/more resources)
- The app will use rule-based classification as fallback
- OR connect to external Ollama API on a VPS

⚠️ **Cold starts** on free tier
- First request after 15 min inactivity: ~10-30 sec
- Solution: Upgrade to paid tier ($7/month) for always-on

---

## Option 2: Deploy Meilisearch Separately

Meilisearch needs to run externally since Render free tier doesn't support Docker containers.

### Option A: Meilisearch Cloud (Easiest)

1. Sign up at [meilisearch.com/cloud](https://www.meilisearch.com/cloud)
2. Create new instance (free trial)
3. Copy URL and API key
4. Add to Render environment variables

**Cost:** $0 for trial, then ~$10/month

### Option B: VPS (Cheapest)

**Recommended VPS:**
- **Hetzner:** €4/month (CAX11)
- **DigitalOcean:** $6/month (Basic Droplet)
- **Linode:** $5/month (Nanode)

**Setup:**

```bash
# SSH into VPS
ssh root@your-vps-ip

# Install Docker
curl -fsSL https://get.docker.com | sh

# Run Meilisearch
docker run -d \
  --name meilisearch \
  -p 7700:7700 \
  -e MEILI_MASTER_KEY=$(openssl rand -base64 32) \
  -v /var/lib/meilisearch:/meili_data \
  --restart unless-stopped \
  getmeili/meilisearch:v1.5

# Configure firewall
ufw allow 7700/tcp
ufw enable

# Get master key
docker logs meilisearch 2>&1 | grep "MEILI_MASTER_KEY"
```

**Cost:** $4-6/month

### Option C: Railway.app (Free)

1. Sign up at [railway.app](https://railway.app)
2. New Project → Deploy Meilisearch
3. Add environment variable: `MEILI_MASTER_KEY`
4. Copy public URL
5. Add to your Render app environment

**Cost:** $0 for 500 hours/month

---

## Option 3: Deploy Ollama (Optional)

To enable AI classification in production, deploy Ollama separately.

### Option A: VPS with GPU (Recommended)

**Providers:**
- **Hetzner Cloud:** ~€40/month (GPU instance)
- **Paperspace:** ~$30/month (GPU compute)
- **RunPod:** ~$0.20/hour (spot instances)

**Setup:**

```bash
# Install Ollama on GPU VPS
curl https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve

# Pull model
ollama pull mistral

# Expose API (use nginx for HTTPS)
sudo apt install nginx
```

**Nginx config:**

```nginx
server {
    listen 443 ssl;
    server_name ollama.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:11434;
    }
}
```

**Update Render env:**
```
OLLAMA_BASE_URL=https://ollama.yourdomain.com
```

**Cost:** $30-40/month

### Option B: Use Cloud LLM API Instead

**Alternative:** Use OpenAI, Anthropic, or other cloud LLM APIs

Modify `app/services/document_processor.py`:

```python
# Instead of Ollama, use OpenAI
import openai

async def _classify_document(self, filename: str, text: str):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    # ... parse response
```

**Cost:** Pay-per-use (~$0.002 per document)

---

## Option 4: Full VPS Deployment

For complete control and better performance.

### Recommended Specs

- **CPU:** 2 cores
- **RAM:** 4GB (8GB with Ollama)
- **Storage:** 20GB SSD
- **Provider:** Hetzner, DigitalOcean, Linode

**Cost:** ~$10-20/month

### Complete Setup

```bash
# 1. SSH into VPS
ssh root@your-vps-ip

# 2. Update system
apt update && apt upgrade -y

# 3. Install Docker
curl -fsSL https://get.docker.com | sh

# 4. Clone repository
git clone https://github.com/yourusername/docugenius.git
cd docugenius

# 5. Create .env file
nano .env
# Add your credentials

# 6. Start services
docker-compose up -d

# 7. Install Python
apt install python3.11 python3.11-venv python3-pip -y

# 8. Install dependencies
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 9. Install Tesseract
apt install tesseract-ocr -y

# 10. Install Ollama
curl https://ollama.ai/install.sh | sh
ollama serve &
ollama pull mistral

# 11. Run with systemd
cat > /etc/systemd/system/docugenius.service << EOF
[Unit]
Description=DocuGenius API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/docugenius
Environment="PATH=/root/docugenius/venv/bin"
ExecStart=/root/docugenius/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 12. Start service
systemctl daemon-reload
systemctl enable docugenius
systemctl start docugenius

# 13. Install Nginx
apt install nginx certbot python3-certbot-nginx -y

# 14. Configure Nginx
cat > /etc/nginx/sites-available/docugenius << EOF
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

ln -s /etc/nginx/sites-available/docugenius /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# 15. Get SSL certificate
certbot --nginx -d yourdomain.com

# 16. Configure firewall
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp
ufw enable
```

### Monitoring

```bash
# Check application status
systemctl status docugenius

# View logs
journalctl -u docugenius -f

# Check resource usage
htop

# Check disk space
df -h
```

---

## Option 5: Docker Deployment

Deploy entire stack with Docker.

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 8000

# Start application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Deploy with Docker Compose

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - MEILISEARCH_URL=http://meilisearch:7700
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - meilisearch
    volumes:
      - ./uploads:/app/uploads

  meilisearch:
    image: getmeili/meilisearch:v1.5
    ports:
      - "7700:7700"
    environment:
      - MEILI_MASTER_KEY=${MEILI_MASTER_KEY}
    volumes:
      - meilisearch_data:/meili_data

  # Optional: Ollama (requires more resources)
  # ollama:
  #   image: ollama/ollama:latest
  #   ports:
  #     - "11434:11434"
  #   volumes:
  #     - ollama_data:/root/.ollama

volumes:
  meilisearch_data:
  # ollama_data:
```

**Deploy:**

```bash
docker-compose up -d
```

---

## Cost Comparison

| Option | Monthly Cost | Performance | Ease |
|--------|-------------|-------------|------|
| **Render Free** | $0 | Good (cold starts) | ⭐⭐⭐⭐⭐ |
| **Render Paid** | $7 | Excellent | ⭐⭐⭐⭐⭐ |
| **VPS Basic** | $5-10 | Good | ⭐⭐⭐ |
| **VPS + GPU** | $30-40 | Excellent | ⭐⭐ |
| **Full Cloud** | $50-100 | Excellent | ⭐⭐⭐⭐ |

---

## Production Checklist

Before going live:

- [ ] Set `DEBUG=False` in environment
- [ ] Use strong `MEILISEARCH_MASTER_KEY`
- [ ] Enable HTTPS/SSL
- [ ] Set up monitoring (UptimeRobot, etc.)
- [ ] Configure backup for Supabase
- [ ] Set up error logging (Sentry, etc.)
- [ ] Configure rate limiting
- [ ] Test upload limits
- [ ] Set up CDN for static files (optional)
- [ ] Configure CORS properly
- [ ] Document API for users
- [ ] Set up CI/CD (GitHub Actions)

---

## Monitoring & Maintenance

### Health Checks

```bash
# Check application health
curl https://your-app.com/health

# Expected response:
{
  "status": "healthy",
  "services": {
    "database": true,
    "search": true,
    "ollama": true
  }
}
```

### Automated Monitoring

Use services like:
- **UptimeRobot** (Free) - Uptime monitoring
- **BetterStack** - Log aggregation
- **Sentry** - Error tracking

### Backups

**Supabase:**
- Automatic backups included
- Download via dashboard if needed

**Meilisearch:**
```bash
# Backup
docker exec meilisearch tar czf /tmp/backup.tar.gz /meili_data
docker cp meilisearch:/tmp/backup.tar.gz ./backup.tar.gz
```

---

## Troubleshooting Production Issues

### High CPU Usage

```bash
# Check processes
htop

# Optimize Ollama
# Use smaller model: llama2:7b instead of mistral
```

### Out of Memory

```bash
# Check memory
free -h

# Restart services
systemctl restart docugenius
docker restart meilisearch
```

### Slow Performance

1. Enable caching in Meilisearch
2. Use CDN for static files
3. Upgrade to paid Render tier (no cold starts)
4. Add database indexing

---

## Support

For deployment help:
- Check [README.md](README.md) troubleshooting
- Open issue on GitHub
- Contact: support@yourdomain.com

---

**Good luck with your deployment! 🚀**

