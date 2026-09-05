-- Add WhatsApp sending fields to sales_pipelines
-- Tracks message delivery status and errors

ALTER TABLE sales_pipelines
ADD COLUMN IF NOT EXISTS message_sent_at TIMESTAMP,
ADD COLUMN IF NOT EXISTS whatsapp_message_id TEXT,
ADD COLUMN IF NOT EXISTS delivery_status TEXT,
ADD COLUMN IF NOT EXISTS last_error TEXT;

COMMENT ON COLUMN sales_pipelines.message_sent_at IS 'Timestamp when message was sent';
COMMENT ON COLUMN sales_pipelines.whatsapp_message_id IS 'WhatsApp API message ID';
COMMENT ON COLUMN sales_pipelines.delivery_status IS 'Status: pending, sent, delivered, failed';
COMMENT ON COLUMN sales_pipelines.last_error IS 'Last error message if sending failed';
