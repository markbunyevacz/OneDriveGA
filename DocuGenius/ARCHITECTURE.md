# 🏗️ DocuGenius Architecture

Technical architecture and design decisions for DocuGenius.

---

## System Overview

DocuGenius is a document management system that uses AI to automatically classify and index documents. The system is designed to be:

- **Free:** $0/month for small deployments
- **Privacy-first:** All processing can be done locally
- **Scalable:** From 10 to 10,000+ documents
- **Modular:** Each component can be replaced independently

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│  • Web Browser (HTML/JS)                                     │
│  • API Clients (curl, Postman, Python, etc.)                │
│  • Mobile Apps (future)                                      │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTPS
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         FastAPI Web Server (Python)                 │   │
│  │  • REST API endpoints                               │   │
│  │  • Request validation (Pydantic)                    │   │
│  │  • Error handling                                   │   │
│  │  • Async/await support                              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     SERVICE LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Document    │  │   Database   │  │    Search    │     │
│  │  Processor   │  │   Service    │  │   Service    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
         ↓                   ↓                   ↓
┌─────────────────────────────────────────────────────────────┐
│                   INFRASTRUCTURE LAYER                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Tesseract │  │  Ollama  │  │Supabase  │  │Meili-    │   │
│  │   OCR    │  │   LLM    │  │PostgreSQL│  │ search   │   │
│  │  (Free)  │  │  (Free)  │  │  (Free)  │  │  (Free)  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. FastAPI Application (`app/main.py`)

**Responsibilities:**
- HTTP request handling
- Route definitions
- Dependency injection
- CORS configuration
- Error handling
- API documentation (OpenAPI/Swagger)

**Key Features:**
- Async/await for non-blocking I/O
- Automatic request validation
- Type hints with Pydantic
- Built-in OpenAPI documentation

**Endpoints:**
- `GET /` - Web UI
- `POST /upload` - Upload & process document
- `GET /search` - Search documents
- `GET /documents` - List all documents
- `GET /documents/{id}` - Get specific document
- `DELETE /documents/{id}` - Delete document
- `GET /health` - Health check

### 2. Document Processor Service (`app/services/document_processor.py`)

**Responsibilities:**
- Text extraction from various formats
- OCR processing for images
- AI classification via LLM
- Rule-based fallback classification

**Supported Formats:**
- PDF (via PyPDF2)
- DOCX (via python-docx)
- Images (PNG, JPG via Tesseract)
- Text files

**Processing Pipeline:**
```
Upload → Extract Text → Classify → Return Structured Data
         ↓              ↓
      Tesseract      Ollama LLM
       (OCR)      (or rule-based)
```

**Classification Fields:**
- `country`: List of country codes
- `technology`: List of technologies
- `product`: List of products
- `document_type`: Category (marketing, technical, etc.)
- `confidence`: 0.0-1.0 confidence score

### 3. Database Service (`app/services/database.py`)

**Responsibilities:**
- CRUD operations
- Document metadata storage
- Query optimization
- Connection management

**Schema:**
```sql
documents (
  id UUID PRIMARY KEY,
  filename TEXT,
  file_type TEXT,
  file_size INTEGER,
  content TEXT,
  country TEXT[],
  technology TEXT[],
  product TEXT[],
  document_type TEXT,
  confidence REAL,
  status TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

**Indexes:**
- `idx_documents_filename` - Fast filename lookup
- `idx_documents_document_type` - Filter by type
- `idx_documents_created_at` - Sort by date
- `idx_documents_country` - GIN index for array search
- `idx_documents_content_search` - Full-text search

### 4. Search Service (`app/services/search.py`)

**Responsibilities:**
- Document indexing
- Full-text search
- Faceted filtering
- Typo tolerance

**Meilisearch Features:**
- Sub-50ms search response
- Typo tolerance (up to 2 typos)
- Prefix search
- Faceted filters
- Highlighting
- Relevance scoring

**Search Strategy:**
```
User Query → Meilisearch → Filter Results → Return to Client
                ↓
         Indexed Fields:
         - filename
         - content
         - document_type
         - country, technology, product
```

---

## Data Flow

### Upload & Processing Flow

```
1. Client uploads file
   ↓
2. FastAPI validates file type and size
   ↓
3. Document Processor extracts text
   ├─ PDF → PyPDF2
   ├─ DOCX → python-docx
   └─ Image → Tesseract OCR
   ↓
4. AI Classification (Ollama)
   ├─ Success → Use AI results
   └─ Failure → Use rule-based fallback
   ↓
5. Store in Supabase
   ↓
6. Index in Meilisearch
   ↓
7. Return response to client
```

### Search Flow

```
1. Client sends search query
   ↓
2. FastAPI validates parameters
   ↓
3. Search Service queries Meilisearch
   ├─ Full-text search
   ├─ Apply filters (country, type, etc.)
   └─ Sort by relevance
   ↓
4. Return results to client
```

---

## Design Decisions

### Why FastAPI?

- **Performance:** Async/await support for high concurrency
- **Type Safety:** Built-in validation with Pydantic
- **Documentation:** Auto-generated OpenAPI/Swagger docs
- **Modern:** Python 3.11+ features
- **Ecosystem:** Large community and packages

### Why Supabase PostgreSQL?

- **Free Tier:** 500MB storage, unlimited API requests
- **Features:** Full PostgreSQL with PostGIS, full-text search
- **Managed:** No database administration needed
- **Scalable:** Easy to upgrade when needed
- **Real-time:** WebSocket subscriptions (future feature)

### Why Ollama?

- **Free:** 100% free, runs locally
- **Privacy:** Data never leaves your infrastructure
- **Quality:** Good accuracy with 7B parameter models
- **Offline:** Works without internet
- **Models:** Mistral, Llama2, Code Llama, etc.

### Why Tesseract?

- **Free:** Open-source (Apache 2.0)
- **Mature:** 30+ years of development
- **Accuracy:** 90%+ for clean documents
- **Languages:** 100+ languages supported
- **No API:** No per-page costs

### Why Meilisearch?

- **Fast:** <50ms search response
- **Easy:** Simple REST API
- **Features:** Typo tolerance, filters, facets
- **Free:** Self-hosted, no limitations
- **Lightweight:** Low memory footprint

---

## Security Considerations

### Authentication

Currently, the system has no authentication. For production, consider:

1. **API Keys:**
```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.API_KEY:
        raise HTTPException(403, "Invalid API key")
```

2. **JWT Tokens:**
```python
from fastapi import Depends
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(credentials = Depends(security)):
    # Verify JWT token
    pass
```

3. **Supabase Auth:**
- Use Supabase's built-in authentication
- Row-level security policies

### File Upload Security

Current protections:
- File type validation
- Size limits (10MB default)
- Content-type checking

Recommended additions:
- Virus scanning (ClamAV)
- Content validation
- Rate limiting
- User quotas

### Data Privacy

- Document content stored in database
- Consider encryption at rest
- GDPR compliance considerations
- Data retention policies

---

## Performance Optimization

### Current Performance

| Operation | Time | Throughput |
|-----------|------|------------|
| PDF upload & process | 2-5s | ~20 docs/min |
| DOCX upload & process | 1-3s | ~30 docs/min |
| Image OCR | 3-10s | ~10 docs/min |
| Search query | <100ms | 1000+ req/s |
| Document listing | <50ms | 2000+ req/s |

### Optimization Strategies

**1. Caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_document_cached(doc_id: str):
    return db_service.get_document(doc_id)
```

**2. Background Processing:**
```python
from fastapi import BackgroundTasks

@app.post("/upload")
async def upload(file: UploadFile, background_tasks: BackgroundTasks):
    # Quick response
    background_tasks.add_task(process_document, file)
    return {"status": "queued"}
```

**3. Database Optimization:**
- Connection pooling
- Query optimization
- Proper indexing
- Materialized views for analytics

**4. CDN for Static Assets:**
- Serve frontend from CDN
- Cache API responses
- Edge caching

---

## Scaling Strategy

### Phase 1: Single Server (0-1000 docs)
- Current architecture
- All services on one machine
- Cost: $0-5/month

### Phase 2: Distributed Services (1000-10000 docs)
- Separate servers for:
  - Application (Render/Railway)
  - Meilisearch (VPS)
  - Ollama (GPU VPS)
- Load balancer
- Cost: $20-50/month

### Phase 3: Horizontal Scaling (10000+ docs)
- Multiple application instances
- Database replication
- Message queue (Redis, RabbitMQ)
- Object storage (S3, R2)
- Kubernetes orchestration
- Cost: $100-500/month

---

## Future Enhancements

### Short-term (1-3 months)
- [ ] User authentication
- [ ] Batch upload
- [ ] Advanced filters
- [ ] Export to Excel/CSV
- [ ] Email notifications
- [ ] API rate limiting

### Medium-term (3-6 months)
- [ ] OneDrive integration
- [ ] Google Drive integration
- [ ] Multi-language OCR
- [ ] Document versioning
- [ ] Collaborative annotations
- [ ] Advanced analytics dashboard

### Long-term (6-12 months)
- [ ] Mobile app (React Native)
- [ ] Real-time collaboration
- [ ] Custom AI models
- [ ] Workflow automation
- [ ] Integration marketplace
- [ ] Enterprise features (SSO, RBAC)

---

## Technology Stack Summary

| Component | Technology | License | Cost |
|-----------|-----------|---------|------|
| **Backend** | FastAPI | MIT | Free |
| **Language** | Python 3.11+ | PSF | Free |
| **Database** | Supabase PostgreSQL | Apache 2.0 | Free tier |
| **Search** | Meilisearch | MIT | Free |
| **OCR** | Tesseract | Apache 2.0 | Free |
| **LLM** | Ollama (Mistral) | MIT | Free |
| **Deployment** | Render.com | - | Free tier |
| **Total** | - | - | **$0/month** |

---

## Contributing

See main [README.md](README.md) for contribution guidelines.

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Supabase Docs](https://supabase.com/docs)
- [Meilisearch Docs](https://docs.meilisearch.com/)
- [Ollama Documentation](https://ollama.ai/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

---

**Last Updated:** December 2025

