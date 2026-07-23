import os
import json
from typing import Dict, Any, Optional


class AIService:
    """Provider-agnostic AI service for company analysis"""
    
    def __init__(self, provider: str = "openai"):
        import threading
        
        # DIAGNOSTIC: Print execution context
        api_key = os.getenv("OPENAI_API_KEY")
        print(f"[AIService.__init__] DIAGNOSTIC:")
        print(f"  API Key (first 15): {api_key[:15] if api_key else 'None'}")
        print(f"  API Key is None: {api_key is None}")
        print(f"  Thread name: {threading.current_thread().name}")
        print(f"  Process ID: {os.getpid()}")
        print(f"  Provider: {provider}")
        
        self.provider = provider
        
        if provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
            self.model = "gpt-4o-mini"  # Most economical option
            print(f"  Model: {self.model}")
        elif provider == "claude":
            from anthropic import Anthropic
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = "claude-3-5-sonnet-20241022"
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")
    
    def analyze_company(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a company and return structured insights.
        
        Args:
            company_data: Dict containing all company information
        
        Returns:
            Dict with AI analysis results
        """
        prompt = self._build_analysis_prompt(company_data)
        
        if self.provider == "openai":
            return self._call_openai(prompt)
        elif self.provider == "claude":
            return self._call_claude(prompt)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _build_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """Build the analysis prompt from company data"""
        
        # Extract data
        name = data.get('name', 'Unknown')
        industry = data.get('industry', 'Unknown')
        location = data.get('location', 'Unknown')
        website = data.get('website', 'No website')
        phone = data.get('phone', 'No phone')
        address = data.get('address', 'No address')
        rating = data.get('rating', 'No rating')
        review_count = data.get('review_count', 0)
        emails = data.get('emails', [])
        social_links = data.get('social_links', {})
        features = data.get('features', {})
        recommended_services = data.get('recommended_services', [])
        
        # Build features summary
        features_list = [k.replace('has_', '').replace('_', ' ') 
                        for k, v in features.items() if v]
        features_text = ', '.join(features_list) if features_list else 'None detected'
        
        # Build social media summary
        social_text = ', '.join(social_links.keys()) if social_links else 'None'
        
        prompt = f"""Eres un Consultor Senior de Transformación Digital en SpineDev con más de 10 años de experiencia en:
- Diseño Web & UX/UI
- SEO & Marketing Digital
- Estrategia de Ventas & CRM
- Automatización con IA & WhatsApp
- Optimización de Procesos de Negocio

Tu misión: Analizar esta empresa objetivamente y generar una evaluación comercial completa EN ESPAÑOL.

REGLAS CRÍTICAS:
✓ Sé brutalmente honesto - si su sitio web es excelente, dilo
✓ NUNCA inventes problemas que no existen
✓ Solo recomienda servicios respaldados por evidencia
✓ Piensa como consultor, no como vendedor
✓ Si no hay suficientes datos, indícalo explícitamente
✓ TODO debe estar en ESPAÑOL

═══════════════════════════════════════════════════════════════
COMPANY DATA
═══════════════════════════════════════════════════════════════

Business: {name}
Industry: {industry}
Location: {location}
Website: {website}
Phone: {phone}
Address: {address}
Google Rating: {rating} ⭐ ({review_count} reviews)

Digital Footprint:
- Emails: {', '.join(emails) if emails else 'None found'}
- Social Media: {social_text}
- Website Features: {features_text}
- Initial Recommendations: {', '.join(recommended_services) if recommended_services else 'None'}

═══════════════════════════════════════════════════════════════
REQUIRED ANALYSIS
═══════════════════════════════════════════════════════════════

IMPORTANTE: Basa tu análisis en los datos disponibles.
NUNCA hagas suposiciones sin evidencia.
SIEMPRE cita datos específicos cuando los tengas disponibles.

1. RESUMEN EJECUTIVO (2-3 párrafos máximo)
   Escribe una evaluación concisa que cubra:
   - Qué tipo de negocio es
   - Calidad de presencia digital actual
   - Puntos más fuertes (específicos)
   - Puntos más débiles (solo basados en evidencia)
   - Mayor oportunidad de crecimiento
   
   IMPORTANTE: Máximo 3 párrafos cortos. Sé directo.

2. EVALUACIÓN DEL SITIO WEB
   Evalúa objetivamente y proporciona:
   - website_score (0-100)
   - Una conclusión breve (máximo 2 oraciones)
   
   Si no hay datos suficientes, indica: "No se puede evaluar - sin datos del sitio web"

3. OPORTUNIDADES DE NEGOCIO
   Identifica oportunidades REALES como:
   - No se detectó chatbot
   - No hay automatización de WhatsApp
   - CRM débil o inexistente
   - No hay sistema de reservas online
   - Falta asistente con IA
   - Flujo de conversión pobre
   - Diseño desactualizado que afecta credibilidad
   
   Solo lista oportunidades JUSTIFICADAS por los datos.
   Cada oportunidad debe ser una oración corta y específica.

4. SERVICIOS RECOMENDADOS DE SPINEDEV
   Para cada servicio, proporciona:
   - Nombre del servicio
   - Por qué tiene sentido (razonamiento específico, máximo 1 oración)
   - Impacto esperado en el negocio (máximo 1 oración)
   - Prioridad de implementación (Alta/Media/Baja)
   
   Ejemplos: Chatbot con IA, Automatización WhatsApp, Rediseño Web, 
   Landing Page, Integración CRM, Sistema de Captura de Leads, SEO, etc.
   
   Si la empresa ya tiene excelente presencia digital, 
   NO recomiendes NADA o solo optimizaciones menores.

5. PUNTUACIÓN DE LEAD (0-100)
   Califica basándote en:
   - Tamaño del negocio y reseñas (más grande = más presupuesto)
   - Madurez digital (desactualizado = más oportunidad)
   - Potencial de crecimiento
   - Probabilidad de cierre
   
   Señales positivas: muchas reseñas, negocio activo, tecnología desactualizada
   Señales negativas: ya moderno, poco valor que agregar
   
   Explica tu puntuación claramente en 1-2 oraciones.

6. CORREO PERSONALIZADO
   Escribe un correo completo que:
   - Mencione algo ESPECÍFICO de su negocio
   - Suene natural, no como plantilla
   - Profesional pero no insistente
   - Se enfoque en valor, no en características
   - Incluya un CTA suave
   
   Línea de asunto + cuerpo completo.
   Máximo 4 párrafos cortos.

7. MENSAJE DE LINKEDIN
   Versión más corta (2-3 oraciones).
   Personalizado. Profesional. Natural.

8. MENSAJE DE WHATSAPP
   Aún más corto (1-2 oraciones).
   Amigable. Conversacional. No vendedor.

9. GUION DE LLAMADA
   Estructura:
   - Apertura (15 segundos)
   - Preguntas de descubrimiento (2-3)
   - Propuesta de valor (30 segundos)
   - Cierre suave / siguiente paso
   
   Que suene natural, no robótico.

10. POSIBLES OBJECIONES
    Predice 3-5 objeciones probables con respuestas:
    - "Ya tenemos un proveedor"
    - "No tenemos presupuesto ahora"
    - "Nuestro sitio web está bien"
    - "Estamos muy ocupados"
    - etc.

11. SIGUIENTE MEJOR ACCIÓN
    Recomienda el paso inmediato siguiente:
    - Enviar correo personalizado
    - Solicitud de conexión en LinkedIn
    - Mensaje por WhatsApp
    - Llamada telefónica directa
    - Esperar X días y hacer seguimiento
    - Agendar reunión de descubrimiento
    
    Sé específico y accionable. Una sola oración.

═══════════════════════════════════════════════════════════════
OUTPUT FORMAT
═══════════════════════════════════════════════════════════════

Devuelve SOLO JSON válido con esta estructura EXACTA (TODO EN ESPAÑOL):

{{
  "executive_summary": "2-3 párrafos máximo, resumen ejecutivo conciso",
  "website_score": 75,
  "website_assessment": "Conclusión breve del sitio web (máximo 2 oraciones)",
  "business_opportunities": [
    "Oportunidad 1 con razonamiento específico (1 oración)",
    "Oportunidad 2 con razonamiento específico (1 oración)"
  ],
  "recommended_services": [
    {{
      "service": "Nombre del Servicio",
      "why": "Justificación específica (1 oración)",
      "impact": "Impacto esperado en el negocio (1 oración)",
      "priority": "Alta|Media|Baja"
    }}
  ],
  "lead_score": 75,
  "score_reasoning": "Explicación clara de la puntuación (1-2 oraciones)",
  "cold_email_subject": "Asunto del correo",
  "cold_email_body": "Correo personalizado completo (máximo 4 párrafos cortos)",
  "linkedin_message": "Mensaje de LinkedIn (2-3 oraciones)",
  "whatsapp_message": "Mensaje de WhatsApp (1-2 oraciones)",
  "cold_call_script": "Guion de llamada completo con estructura",
  "possible_objections": [
    {{
      "objection": "Texto de la objeción",
      "response": "Cómo manejarla"
    }}
  ],
  "next_best_action": "Siguiente paso inmediato específico (1 oración)"
}}

Devuelve SOLO el JSON. Sin markdown. Sin explicación. Sin bloques de código."""

        return prompt
    
    def _call_openai(self, prompt: str) -> Dict[str, Any]:
        """Call OpenAI API and return structured response"""
        import threading
        
        # DIAGNOSTIC: Print before API call
        api_key = os.getenv("OPENAI_API_KEY")
        prompt_length = len(prompt)
        estimated_tokens = prompt_length // 4
        
        print(f"[AIService._call_openai] DIAGNOSTIC:")
        print(f"  API Key (first 15): {api_key[:15] if api_key else 'None'}")
        print(f"  Model: {self.model}")
        print(f"  Prompt length: {prompt_length}")
        print(f"  Estimated tokens: {estimated_tokens}")
        print(f"  Thread name: {threading.current_thread().name}")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": "You are a Senior Digital Transformation Consultant. Return only valid JSON."
                }, {
                    "role": "user",
                    "content": prompt
                }],
                temperature=0.7,
                max_tokens=4000,
                response_format={"type": "json_object"}  # Force JSON response
            )
            
            # Extract JSON from response
            content = response.choices[0].message.content
            print(f"[AIService] AI Response length: {len(content)}")
            print(f"[AIService] AI Response preview: {content[:500]}")
            
            result = json.loads(content)
            print(f"[AIService] Parsed JSON keys: {list(result.keys())}")
            print(f"[AIService] Lead score: {result.get('lead_score')}")
            
            return result
        
        except Exception as e:
            print(f"[AIService] ERROR: {str(e)}")
            raise Exception(f"AI analysis failed: {str(e)}")
    
    def _call_claude(self, prompt: str) -> Dict[str, Any]:
        """Call Claude API and return structured response"""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Extract JSON from response
            content = response.content[0].text
            
            # Try to parse as JSON
            try:
                result = json.loads(content)
                return result
            except json.JSONDecodeError:
                # If response is not pure JSON, try to extract it
                # Look for JSON block
                if '{' in content and '}' in content:
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    json_str = content[start:end]
                    result = json.loads(json_str)
                    return result
                else:
                    raise ValueError("Response is not valid JSON")
        
        except Exception as e:
            raise Exception(f"AI analysis failed: {str(e)}")
