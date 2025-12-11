"""Supabase database service"""

from supabase import create_client, Client
from typing import Optional, List, Dict, Any
from loguru import logger
import uuid
from datetime import datetime

from app.config import settings


class DatabaseService:
    """Handle all database operations with Supabase"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.table_name = "documents"
    
    async def initialize(self):
        """Initialize Supabase client and create table if needed"""
        try:
            self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            
            # Try to create table (will fail silently if exists)
            await self._create_table_if_not_exists()
            
            logger.info("Supabase database initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    async def _create_table_if_not_exists(self):
        """Create documents table if it doesn't exist"""
        # Note: In Supabase, you typically create tables via the web UI or SQL editor
        # This is a placeholder - actual table creation should be done manually
        logger.info("Ensure 'documents' table exists in Supabase")
    
    async def store_document(self, document: Dict[str, Any]) -> str:
        """Store a document in the database"""
        try:
            doc_id = str(uuid.uuid4())
            
            data = {
                "id": doc_id,
                "filename": document["filename"],
                "file_type": document["file_type"],
                "file_size": document["file_size"],
                "content": document["content"][:5000],  # Limit content size
                "country": document["classification"]["country"],
                "technology": document["classification"]["technology"],
                "product": document["classification"]["product"],
                "document_type": document["classification"]["document_type"],
                "confidence": document["classification"]["confidence"],
                "status": document.get("status", "processed"),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            response = self.client.table(self.table_name).insert(data).execute()
            
            logger.info(f"Document stored in database: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"Failed to store document: {e}")
            raise
    
    async def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a document by ID"""
        try:
            response = self.client.table(self.table_name).select("*").eq("id", doc_id).execute()
            
            if response.data:
                doc = response.data[0]
                return self._format_document(doc)
            return None
            
        except Exception as e:
            logger.error(f"Failed to get document {doc_id}: {e}")
            return None
    
    async def list_documents(self, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """List documents with pagination"""
        try:
            response = (
                self.client.table(self.table_name)
                .select("*")
                .order("created_at", desc=True)
                .range(offset, offset + limit - 1)
                .execute()
            )
            
            return [self._format_document(doc) for doc in response.data]
            
        except Exception as e:
            logger.error(f"Failed to list documents: {e}")
            return []
    
    async def delete_document(self, doc_id: str) -> bool:
        """Delete a document"""
        try:
            response = self.client.table(self.table_name).delete().eq("id", doc_id).execute()
            return True
        except Exception as e:
            logger.error(f"Failed to delete document {doc_id}: {e}")
            return False
    
    async def search_by_filters(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search documents by filters"""
        try:
            query = self.client.table(self.table_name).select("*")
            
            for key, value in filters.items():
                if value:
                    query = query.eq(key, value)
            
            response = query.execute()
            return [self._format_document(doc) for doc in response.data]
            
        except Exception as e:
            logger.error(f"Failed to search documents: {e}")
            return []
    
    def _format_document(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Format document for response"""
        return {
            "id": doc["id"],
            "filename": doc["filename"],
            "file_type": doc["file_type"],
            "file_size": doc["file_size"],
            "content": doc["content"],
            "classification": {
                "country": doc["country"],
                "technology": doc["technology"],
                "product": doc["product"],
                "document_type": doc["document_type"],
                "confidence": doc["confidence"]
            },
            "status": doc["status"],
            "created_at": doc["created_at"],
            "updated_at": doc["updated_at"]
        }
    
    async def check_health(self) -> bool:
        """Check database connection health"""
        try:
            # Try to query the table
            self.client.table(self.table_name).select("id").limit(1).execute()
            return True
        except:
            return False

