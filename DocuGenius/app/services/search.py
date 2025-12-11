"""Meilisearch service for document search"""

import meilisearch
from typing import List, Dict, Any, Optional
from loguru import logger

from app.config import settings


class SearchService:
    """Handle document search with Meilisearch"""
    
    def __init__(self):
        self.client: Optional[meilisearch.Client] = None
        self.index_name = "documents"
        self.index: Optional[meilisearch.index.Index] = None
    
    async def initialize(self):
        """Initialize Meilisearch client and index"""
        try:
            self.client = meilisearch.Client(
                settings.MEILISEARCH_URL,
                settings.MEILISEARCH_MASTER_KEY if settings.MEILISEARCH_MASTER_KEY else None
            )
            
            # Create or get index
            try:
                self.index = self.client.get_index(self.index_name)
            except:
                # Create index if doesn't exist
                task = self.client.create_index(self.index_name, {"primaryKey": "id"})
                self.index = self.client.get_index(self.index_name)
            
            # Configure searchable attributes
            self.index.update_searchable_attributes([
                "filename",
                "content",
                "document_type",
                "country",
                "technology",
                "product"
            ])
            
            # Configure filterable attributes
            self.index.update_filterable_attributes([
                "country",
                "technology",
                "product",
                "document_type",
                "file_type"
            ])
            
            logger.info("Meilisearch initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Meilisearch: {e}")
            logger.warning("Search functionality will be limited")
    
    async def index_document(self, document: Dict[str, Any]):
        """Add document to search index"""
        try:
            if not self.index:
                logger.warning("Meilisearch not available, skipping indexing")
                return
            
            search_doc = {
                "id": document.get("id"),
                "filename": document["filename"],
                "content": document["content"][:5000],  # Limit content
                "file_type": document["file_type"],
                "country": document["classification"]["country"],
                "technology": document["classification"]["technology"],
                "product": document["classification"]["product"],
                "document_type": document["classification"]["document_type"]
            }
            
            self.index.add_documents([search_doc])
            logger.info(f"Document indexed: {document['filename']}")
            
        except Exception as e:
            logger.error(f"Failed to index document: {e}")
    
    async def search(
        self, 
        query: str, 
        filters: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search documents"""
        try:
            if not self.index:
                logger.warning("Meilisearch not available")
                return []
            
            search_params = {
                "limit": limit
            }
            
            if filters:
                search_params["filter"] = filters
            
            results = self.index.search(query, search_params)
            
            return results.get("hits", [])
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    async def delete_document(self, doc_id: str):
        """Remove document from search index"""
        try:
            if self.index:
                self.index.delete_document(doc_id)
                logger.info(f"Document removed from index: {doc_id}")
        except Exception as e:
            logger.error(f"Failed to delete from index: {e}")
    
    async def check_health(self) -> bool:
        """Check Meilisearch connection"""
        try:
            if self.client:
                self.client.health()
                return True
            return False
        except:
            return False

