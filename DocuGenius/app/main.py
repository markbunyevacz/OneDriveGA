"""Main FastAPI application"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import uvicorn
from loguru import logger
import sys

from app.config import settings
from app.services.document_processor import DocumentProcessor
from app.services.database import DatabaseService
from app.services.search import SearchService
from app.models.document import DocumentResponse, DocumentClassification, SearchRequest

# Configure logging
logger.remove()
logger.add(sys.stderr, level="INFO" if not settings.DEBUG else "DEBUG")

# Initialize FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Document Management System - Completely Free Stack"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
doc_processor = DocumentProcessor()
db_service = DatabaseService()
search_service = SearchService()


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Initialize database
    await db_service.initialize()
    logger.info("✓ Database initialized")
    
    # Initialize search
    await search_service.initialize()
    logger.info("✓ Search index initialized")
    
    # Check Ollama connection
    if await doc_processor.check_ollama():
        logger.info("✓ Ollama connected")
    else:
        logger.warning("⚠ Ollama not available - classification will be limited")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Landing page with upload form"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DocuGenius - Free Document Management</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 40px;
                backdrop-filter: blur(10px);
            }
            h1 { margin: 0 0 10px 0; }
            .subtitle { opacity: 0.9; margin-bottom: 30px; }
            .upload-form {
                background: white;
                color: #333;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            }
            input[type="file"] {
                width: 100%;
                padding: 15px;
                border: 2px dashed #667eea;
                border-radius: 5px;
                margin-bottom: 20px;
                cursor: pointer;
            }
            button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
                width: 100%;
            }
            button:hover { opacity: 0.9; }
            .features {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                margin-top: 30px;
            }
            .feature {
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 10px;
            }
            .feature h3 { margin-top: 0; }
            #result {
                margin-top: 20px;
                padding: 15px;
                border-radius: 5px;
                display: none;
            }
            .success { background: #10b981; }
            .error { background: #ef4444; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📄 DocuGenius</h1>
            <p class="subtitle">AI-Powered Document Management - Completely Free Stack</p>
            
            <div class="upload-form">
                <h2>Upload Document</h2>
                <form id="uploadForm">
                    <input type="file" id="fileInput" accept=".pdf,.docx,.xlsx,.txt,.png,.jpg,.jpeg" required>
                    <button type="submit">🚀 Upload & Process</button>
                </form>
                <div id="result"></div>
            </div>
            
            <div class="features">
                <div class="feature">
                    <h3>🤖 AI Classification</h3>
                    <p>Ollama LLM (Mistral) - 100% Free</p>
                </div>
                <div class="feature">
                    <h3>🔍 Smart Search</h3>
                    <p>Meilisearch - Self-hosted</p>
                </div>
                <div class="feature">
                    <h3>📝 OCR Processing</h3>
                    <p>Tesseract - Open Source</p>
                </div>
                <div class="feature">
                    <h3>💾 PostgreSQL</h3>
                    <p>Supabase Free Tier</p>
                </div>
            </div>
        </div>
        
        <script>
            document.getElementById('uploadForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const fileInput = document.getElementById('fileInput');
                const result = document.getElementById('result');
                const file = fileInput.files[0];
                
                if (!file) return;
                
                const formData = new FormData();
                formData.append('file', file);
                
                result.style.display = 'block';
                result.className = '';
                result.innerHTML = '⏳ Processing...';
                
                try {
                    const response = await fetch('/upload', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        result.className = 'success';
                        result.innerHTML = `
                            ✅ Success!<br>
                            <strong>Filename:</strong> ${data.filename}<br>
                            <strong>Type:</strong> ${data.classification.document_type}<br>
                            <strong>Country:</strong> ${data.classification.country.join(', ')}<br>
                            <strong>Technology:</strong> ${data.classification.technology.join(', ')}<br>
                            <strong>Confidence:</strong> ${(data.classification.confidence * 100).toFixed(1)}%
                        `;
                    } else {
                        throw new Error(data.detail || 'Upload failed');
                    }
                } catch (error) {
                    result.className = 'error';
                    result.innerHTML = `❌ Error: ${error.message}`;
                }
            });
        </script>
    </body>
    </html>
    """


@app.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document
    
    - Extracts text (OCR if needed)
    - Classifies using AI
    - Stores in database
    - Indexes for search
    """
    try:
        logger.info(f"Processing upload: {file.filename}")
        
        # Validate file
        file_ext = "." + file.filename.split(".")[-1].lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(400, f"File type {file_ext} not allowed")
        
        # Process document
        result = await doc_processor.process_document(file)
        
        # Store in database
        doc_id = await db_service.store_document(result)
        result["id"] = doc_id
        
        # Index for search
        await search_service.index_document(result)
        
        logger.info(f"✓ Document processed: {file.filename} (ID: {doc_id})")
        
        return DocumentResponse(**result)
        
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise HTTPException(500, f"Processing failed: {str(e)}")


@app.get("/search", response_model=List[DocumentResponse])
async def search_documents(
    q: str = Query(..., description="Search query"),
    country: Optional[str] = Query(None, description="Filter by country"),
    technology: Optional[str] = Query(None, description="Filter by technology"),
    document_type: Optional[str] = Query(None, description="Filter by document type"),
    limit: int = Query(10, ge=1, le=100, description="Maximum results")
):
    """
    Search documents with filters
    
    - Full-text search using Meilisearch
    - Filter by country, technology, document type
    - Fast results (<100ms)
    """
    try:
        filters = []
        if country:
            filters.append(f"country = '{country}'")
        if technology:
            filters.append(f"technology = '{technology}'")
        if document_type:
            filters.append(f"document_type = '{document_type}'")
        
        results = await search_service.search(q, filters, limit)
        
        return [DocumentResponse(**doc) for doc in results]
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise HTTPException(500, f"Search failed: {str(e)}")


@app.get("/documents", response_model=List[DocumentResponse])
async def list_documents(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """List all documents with pagination"""
    try:
        documents = await db_service.list_documents(limit, offset)
        return [DocumentResponse(**doc) for doc in documents]
    except Exception as e:
        logger.error(f"List error: {str(e)}")
        raise HTTPException(500, f"Failed to list documents: {str(e)}")


@app.get("/documents/{doc_id}", response_model=DocumentResponse)
async def get_document(doc_id: str):
    """Get a specific document by ID"""
    try:
        document = await db_service.get_document(doc_id)
        if not document:
            raise HTTPException(404, "Document not found")
        return DocumentResponse(**document)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get document error: {str(e)}")
        raise HTTPException(500, f"Failed to get document: {str(e)}")


@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document"""
    try:
        success = await db_service.delete_document(doc_id)
        if not success:
            raise HTTPException(404, "Document not found")
        
        # Remove from search index
        await search_service.delete_document(doc_id)
        
        return {"status": "success", "message": f"Document {doc_id} deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete error: {str(e)}")
        raise HTTPException(500, f"Failed to delete document: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "services": {
            "database": await db_service.check_health(),
            "search": await search_service.check_health(),
            "ollama": await doc_processor.check_ollama()
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

