"""Document data models"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class DocumentClassification(BaseModel):
    """AI classification results"""
    country: List[str] = Field(default=["Other"], description="Countries mentioned")
    technology: List[str] = Field(default=["Other"], description="Technologies mentioned")
    product: List[str] = Field(default=["Other"], description="Products mentioned")
    document_type: str = Field(default="other", description="Document category")
    confidence: float = Field(default=0.5, ge=0.0, le=1.0, description="Classification confidence")


class DocumentResponse(BaseModel):
    """Document response model"""
    id: Optional[str] = None
    filename: str
    file_type: str
    file_size: int
    content: str
    classification: DocumentClassification
    status: str = "processed"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "filename": "Q4_Marketing.pdf",
                "file_type": "pdf",
                "file_size": 1024000,
                "content": "Marketing strategy for Q4...",
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
        }


class SearchRequest(BaseModel):
    """Search request model"""
    query: str = Field(..., min_length=1, description="Search query")
    filters: Optional[List[str]] = Field(None, description="Filter conditions")
    limit: int = Field(10, ge=1, le=100, description="Maximum results")

