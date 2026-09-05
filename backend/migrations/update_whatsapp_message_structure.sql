-- Update whatsapp_message structure to store template variables
-- This migration updates existing pipelines to use the new template variable format

-- Note: This is a data structure change, not a schema change
-- The whatsapp_message column is JSONB, so we just need to update the data format

-- Example of new structure:
-- {
--   "template_name": "cold_outreach_v2",
--   "variables": [
--     "Observación específica",
--     "Impacto de negocio", 
--     "Beneficio específico"
--   ],
--   "preview": "Hola,\n\nObservación específica\n\nImpacto de negocio\n\nEn SpineDev ayudamos a empresas a Beneficio específico.\n\n¿Tendrías 15 minutos para una llamada esta semana?",
--   "version": 1,
--   "generated_at": "2024-01-01T00:00:00Z"
-- }

-- No SQL changes needed, just documenting the new format
