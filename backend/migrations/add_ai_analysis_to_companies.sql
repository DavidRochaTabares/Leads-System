-- Add AI analysis field to companies table
ALTER TABLE companies
ADD COLUMN IF NOT EXISTS ai_analysis JSONB DEFAULT NULL,
ADD COLUMN IF NOT EXISTS ai_analyzed_at TIMESTAMP;

-- Add index for querying companies that need AI analysis
CREATE INDEX IF NOT EXISTS idx_companies_ai_not_analyzed 
ON companies (website_scraped_at) 
WHERE website_scraped_at IS NOT NULL AND ai_analyzed_at IS NULL;
