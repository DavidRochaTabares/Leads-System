-- Add website enrichment fields to companies table
ALTER TABLE companies
ADD COLUMN IF NOT EXISTS emails JSONB DEFAULT '[]'::jsonb,
ADD COLUMN IF NOT EXISTS social_links JSONB DEFAULT '{}'::jsonb,
ADD COLUMN IF NOT EXISTS features JSONB DEFAULT '{}'::jsonb,
ADD COLUMN IF NOT EXISTS recommended_services JSONB DEFAULT '[]'::jsonb,
ADD COLUMN IF NOT EXISTS website_scraped_at TIMESTAMP;

-- Add index for querying companies that need website scraping
CREATE INDEX IF NOT EXISTS idx_companies_website_not_scraped 
ON companies (website) 
WHERE website IS NOT NULL AND website_scraped_at IS NULL;
