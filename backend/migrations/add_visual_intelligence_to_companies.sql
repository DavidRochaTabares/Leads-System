-- Add visual intelligence fields to companies table

-- Screenshots (store URLs only, not base64)
ALTER TABLE companies ADD COLUMN IF NOT EXISTS screenshot_homepage_desktop TEXT;
ALTER TABLE companies ADD COLUMN IF NOT EXISTS screenshot_homepage_mobile TEXT;
ALTER TABLE companies ADD COLUMN IF NOT EXISTS screenshot_contact TEXT;
ALTER TABLE companies ADD COLUMN IF NOT EXISTS screenshot_services TEXT;
ALTER TABLE companies ADD COLUMN IF NOT EXISTS screenshot_about TEXT;

-- Website metadata
ALTER TABLE companies ADD COLUMN IF NOT EXISTS page_title TEXT;
ALTER TABLE companies ADD COLUMN IF NOT EXISTS meta_description TEXT;
ALTER TABLE companies ADD COLUMN IF NOT EXISTS h1_text TEXT;
ALTER TABLE companies ADD COLUMN IF NOT EXISTS favicon_url TEXT;
ALTER TABLE companies ADD COLUMN IF NOT EXISTS logo_detected BOOLEAN DEFAULT FALSE;
ALTER TABLE companies ADD COLUMN IF NOT EXISTS load_time_seconds FLOAT;

-- Visual features
ALTER TABLE companies ADD COLUMN IF NOT EXISTS has_cta_buttons BOOLEAN DEFAULT FALSE;
ALTER TABLE companies ADD COLUMN IF NOT EXISTS has_floating_whatsapp BOOLEAN DEFAULT FALSE;
ALTER TABLE companies ADD COLUMN IF NOT EXISTS has_booking_system BOOLEAN DEFAULT FALSE;
ALTER TABLE companies ADD COLUMN IF NOT EXISTS primary_cta_text TEXT;

-- Timestamp for visual intelligence capture
ALTER TABLE companies ADD COLUMN IF NOT EXISTS visual_intelligence_captured_at TIMESTAMP;
