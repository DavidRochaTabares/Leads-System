# Visual Website Intelligence Setup

## Overview

The Visual Intelligence system captures screenshots and metadata from company websites to enable AI-powered visual analysis and professional UX/UI audits.

## Features

✅ **Screenshot Capture**
- Homepage Desktop (1440px, full page)
- Homepage Mobile (390px, full page)
- Contact page
- Services page
- About page

✅ **Metadata Extraction**
- Page title
- Meta description
- H1 heading
- Logo detection
- Favicon
- Load time measurement

✅ **Visual Features Detection**
- CTA buttons
- Primary CTA text
- Floating WhatsApp button
- Contact forms
- Booking systems
- Chatbot presence

✅ **AI Analysis Enhancement**
- Evidence-based recommendations
- Visual quality assessment
- UX/UI evaluation
- Conversion opportunity identification

## Database Setup

### 1. Run Visual Intelligence Migration

```bash
# From backend directory
psql -h <your-supabase-host> -U postgres -d postgres -f migrations/add_visual_intelligence_to_companies.sql
```

Or execute in Supabase SQL Editor:
```sql
-- Copy contents from backend/migrations/add_visual_intelligence_to_companies.sql
```

### 2. Create Storage Bucket

Execute in Supabase SQL Editor:
```sql
-- Copy contents from backend/migrations/create_storage_bucket.sql
```

Or create manually in Supabase Dashboard:
1. Go to Storage
2. Create new bucket: `website-screenshots`
3. Set to **Public**
4. Configure policies for public read access

## How It Works

### 1. Screenshot Capture Flow

```
Company Website → Playwright → VisualIntelligence Service → Supabase Storage
                                         ↓
                                  PostgreSQL (URLs only)
```

### 2. Integration Points

**Backend:**
- `services/visual_intelligence.py` - Screenshot capture and metadata extraction
- `services/website_scraper.py` - Integrates visual intelligence
- `services/prospecting_worker.py` - Orchestrates the pipeline
- `repositories/company_repository.py` - Saves visual data
- `services/ai_service.py` - Uses visual data for analysis

**Frontend:**
- `components/website-preview.tsx` - Screenshot gallery with lightbox
- `components/ai-analysis-card.tsx` - Enhanced AI analysis display
- `components/session-companies.tsx` - Main company view

### 3. AI Analysis Enhancement

The AI now receives:
- Structured data (emails, social links, features)
- Website metadata (title, description, H1, load time)
- Visual features (CTAs, WhatsApp, booking, chatbot)
- Screenshot availability confirmation

This enables evidence-based recommendations like:
- ❌ "No se detectó CTA principal en la página de inicio"
- ❌ "Tiempo de carga de 4.2s (debe ser < 3s)"
- ✅ "Tiene WhatsApp flotante para contacto rápido"

## Performance Considerations

### Screenshot Caching
- Screenshots are captured **once** per company
- Stored in Supabase Storage (not database)
- Reused for all subsequent AI analyses
- Only URLs stored in PostgreSQL

### Failure Handling
- Screenshot capture failures **do not** stop mining
- Visual analysis gracefully skipped if no screenshots
- Structured data analysis continues normally

### Storage Optimization
- PNG format for quality
- Full-page screenshots for complete context
- Maximum 5 screenshots per company
- Public URLs for fast CDN delivery

## Testing

### 1. Test Visual Intelligence Standalone

```python
# backend/test_visual_intelligence.py
from services.visual_intelligence import VisualIntelligence
from services.supabase_client import get_supabase
from playwright.sync_api import sync_playwright

supabase = get_supabase()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    visual_intel = VisualIntelligence(page, supabase)
    result = visual_intel.capture_website_intelligence(
        company_id="test-123",
        website_url="https://example.com"
    )
    
    print("Screenshots:", result["screenshots"])
    print("Metadata:", result["metadata"])
    print("Features:", result["visual_features"])
    
    browser.close()
```

### 2. Test Full Pipeline

1. Start backend: `npm run dev`
2. Create prospecting session
3. Monitor logs for "Scraping website + capturing screenshots"
4. Check Supabase Storage for uploaded screenshots
5. Verify AI analysis includes visual evidence

## Troubleshooting

### Screenshots Not Captured

**Check:**
1. Supabase Storage bucket exists and is public
2. Supabase credentials in `.env`
3. Playwright installed: `pip install playwright && playwright install chromium`
4. Website is accessible (not behind auth/firewall)

**Logs to check:**
```
"Visual intelligence capture failed (continuing): ..."
"Screenshot upload error: ..."
```

### AI Not Using Visual Data

**Check:**
1. Database columns exist (run migration)
2. `company_repo.update_website_data()` saves visual fields
3. AI prompt includes Visual Intelligence section
4. Screenshots were successfully captured

### Storage Policies

If screenshots upload but aren't accessible:
```sql
-- Check policies
SELECT * FROM storage.policies WHERE bucket_id = 'website-screenshots';

-- Recreate public access policy
CREATE POLICY "Public Access"
ON storage.objects FOR SELECT
USING (bucket_id = 'website-screenshots');
```

## Architecture Decisions

### Why Supabase Storage?
- ✅ Integrated with existing Supabase setup
- ✅ CDN for fast global delivery
- ✅ Public URLs for easy frontend access
- ✅ No base64 bloat in PostgreSQL

### Why Full-Page Screenshots?
- ✅ Complete visual context for AI
- ✅ Captures below-the-fold content
- ✅ Better UX/UI assessment
- ✅ Mobile responsiveness evaluation

### Why PNG?
- ✅ Lossless quality for text readability
- ✅ Better for UI screenshots than JPEG
- ✅ Acceptable file size for web delivery

## Future Enhancements

- [ ] Screenshot comparison over time
- [ ] Automated accessibility scoring
- [ ] Color palette extraction
- [ ] Typography analysis
- [ ] Mobile vs Desktop comparison view
- [ ] Performance metrics (LCP, FID, CLS)
- [ ] Screenshot regeneration on demand
