-- Supabase Database Schema for DocuGenius
-- Run this in Supabase SQL Editor to create the documents table

-- Create documents table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename TEXT NOT NULL,
    file_type TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    content TEXT,
    country TEXT[] DEFAULT ARRAY['Other'],
    technology TEXT[] DEFAULT ARRAY['Other'],
    product TEXT[] DEFAULT ARRAY['Other'],
    document_type TEXT DEFAULT 'other',
    confidence REAL DEFAULT 0.5,
    status TEXT DEFAULT 'processed',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_documents_filename ON documents(filename);
CREATE INDEX IF NOT EXISTS idx_documents_document_type ON documents(document_type);
CREATE INDEX IF NOT EXISTS idx_documents_created_at ON documents(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_documents_country ON documents USING GIN(country);
CREATE INDEX IF NOT EXISTS idx_documents_technology ON documents USING GIN(technology);

-- Create full-text search index
CREATE INDEX IF NOT EXISTS idx_documents_content_search ON documents USING GIN(to_tsvector('english', content));

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to call the function
CREATE TRIGGER update_documents_updated_at 
    BEFORE UPDATE ON documents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS) - Optional but recommended
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations for authenticated users
-- Modify based on your authentication requirements
CREATE POLICY "Allow all operations for authenticated users" 
    ON documents
    FOR ALL
    TO authenticated
    USING (true)
    WITH CHECK (true);

-- Create policy to allow read-only for anonymous users (optional)
CREATE POLICY "Allow read for anonymous users" 
    ON documents
    FOR SELECT
    TO anon
    USING (true);

-- Grant permissions
GRANT ALL ON documents TO authenticated;
GRANT SELECT ON documents TO anon;

-- Create view for document statistics (optional)
CREATE OR REPLACE VIEW document_stats AS
SELECT 
    COUNT(*) as total_documents,
    COUNT(DISTINCT document_type) as document_types,
    SUM(file_size) as total_size_bytes,
    AVG(confidence) as avg_confidence,
    MAX(created_at) as last_upload
FROM documents;

GRANT SELECT ON document_stats TO authenticated;

-- Sample query to verify setup
-- SELECT * FROM documents ORDER BY created_at DESC LIMIT 10;

