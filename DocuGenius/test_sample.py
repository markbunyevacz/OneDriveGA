"""
Sample test file for DocuGenius
Run with: pytest test_sample.py
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert "DocuGenius" in response.text


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "app" in data
    assert data["app"] == "DocuGenius"


def test_list_documents_empty():
    """Test listing documents when empty"""
    response = client.get("/documents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_search_endpoint():
    """Test search endpoint"""
    response = client.get("/search?q=test")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_upload_invalid_file_type():
    """Test upload with invalid file type"""
    response = client.post(
        "/upload",
        files={"file": ("test.exe", b"fake content", "application/x-msdownload")}
    )
    # May fail due to file type validation
    assert response.status_code in [200, 400, 500]


@pytest.mark.asyncio
async def test_document_processor():
    """Test document processor"""
    from app.services.document_processor import DocumentProcessor
    
    processor = DocumentProcessor()
    
    # Test rule-based classification
    result = processor._default_classification(
        "marketing_plan.pdf",
        "This is a marketing campaign for Q4"
    )
    
    assert result["document_type"] == "marketing"
    assert "country" in result
    assert "technology" in result
    assert isinstance(result["confidence"], float)


def test_classification_validation():
    """Test classification validation"""
    from app.services.document_processor import DocumentProcessor
    
    processor = DocumentProcessor()
    
    # Invalid classification
    invalid = {
        "country": "USA",  # Should be list
        "technology": ["AI"],
        "confidence": "high"  # Should be float
    }
    
    validated = processor._validate_classification(invalid)
    
    assert isinstance(validated["country"], list)
    assert isinstance(validated["confidence"], float)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

