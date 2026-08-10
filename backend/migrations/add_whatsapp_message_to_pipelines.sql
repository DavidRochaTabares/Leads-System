-- Add WhatsApp Message field to sales_pipelines
-- This stores the generated WhatsApp message for each pipeline

ALTER TABLE sales_pipelines
ADD COLUMN IF NOT EXISTS whatsapp_message JSONB;

COMMENT ON COLUMN sales_pipelines.whatsapp_message IS 'Generated WhatsApp message with status, version, and content';

-- Example structure:
-- {
--   "status": "ready",
--   "generated_at": "2024-01-01T00:00:00Z",
--   "message": "Hola...",
--   "version": 1
-- }
