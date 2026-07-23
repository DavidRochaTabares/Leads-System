import os
import json
from typing import Dict, Any
from openai import OpenAI


class SalesStrategyEngine:
    """
    Sales Strategy Engine - Independent AI Module
    
    Responsibility: Answer "How should SpineDev sell to this company?"
    
    NOT: "What does this company need?" (that's AI Analysis)
    
    Consumes:
    - Company information
    - Website data
    - AI Analysis
    - Lead Score
    
    Never scrapes. Never analyzes websites again.
    """
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        self.client = OpenAI(api_key=api_key)
    
    def generate_strategy(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate commercial strategy for a company
        
        Args:
            company_data: {
                'name': str,
                'industry': str,
                'location': str,
                'website': str,
                'ai_analysis': dict,  # From AI Analysis
                'lead_score': int,
                'emails': list,
                'social_links': dict,
                'features': dict
            }
        
        Returns:
            Commercial strategy (JSON)
        """
        print(f"[STRATEGY ENGINE] Generating strategy for {company_data.get('name')}")
        
        prompt = self._build_strategy_prompt(company_data)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un estratega comercial experto de SpineDev. Tu trabajo es diseñar estrategias de venta personalizadas basadas en análisis de empresas. Respondes SOLO en formato JSON válido."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            strategy = json.loads(content)
            
            print(f"[STRATEGY ENGINE] Strategy generated successfully")
            return strategy
            
        except Exception as e:
            print(f"[STRATEGY ENGINE ERROR] {str(e)}")
            raise Exception(f"Strategy generation failed: {str(e)}")
    
    def _build_strategy_prompt(self, company_data: Dict[str, Any]) -> str:
        """Build the strategy generation prompt"""
        
        name = company_data.get('name', 'Desconocido')
        industry = company_data.get('industry', 'No especificado')
        location = company_data.get('location', 'No especificado')
        website = company_data.get('website', 'No disponible')
        
        # Extract AI Analysis
        ai_analysis = company_data.get('ai_analysis', {})
        lead_score = ai_analysis.get('lead_score', 50)
        executive_summary = ai_analysis.get('executive_summary', 'No disponible')
        business_opportunities = ai_analysis.get('business_opportunities', [])
        recommended_services = ai_analysis.get('recommended_services', [])
        
        # Extract website features
        features = company_data.get('features', {})
        emails = company_data.get('emails', [])
        social_links = company_data.get('social_links', {})
        
        prompt = f"""
Eres un GERENTE DE VENTAS SENIOR de SpineDev preparando a un vendedor para primer contacto.

SITUACIÓN:
El vendedor va a enviar un mensaje a esta empresa en los próximos 30 segundos.

TU TRABAJO:
Crear un CHEAT SHEET de una página con todo lo que necesita saber.

NO escribas reportes.
NO repitas análisis.
NO uses lenguaje genérico.

Piensa: "¿Qué información ayudará a cerrar esta venta?"

=== PROSPECTO ===

EMPRESA: {name}
INDUSTRIA: {industry}
UBICACIÓN: {location}
LEAD SCORE: {lead_score}/100

ANÁLISIS:
{executive_summary}

OPORTUNIDADES:
{json.dumps(business_opportunities, indent=2, ensure_ascii=False)}

SERVICIOS SUGERIDOS:
{json.dumps(recommended_services, indent=2, ensure_ascii=False)}

TECNOLOGÍA:
- Emails: {len(emails)}
- Redes: {', '.join(social_links.keys()) if social_links else 'Ninguna'}
- Chatbot: {'Sí' if features.get('chatbot') else 'No'}
- WhatsApp: {'Sí' if features.get('whatsapp') else 'No'}

=== INSTRUCCIONES ===

1. ¿QUÉ VENDER?
   - Servicio principal
   - Servicio secundario (opcional)
   - Oportunidad: Low/Medium/High
   - **WHY THIS SERVICE?** (3 justificaciones específicas)
     Ejemplo: "La comunicación con clientes parece ser manual"
     NO: "Necesitan tecnología"

2. ¿POR QUÉ ESTA EMPRESA?
   - 3 razones (máx 10 palabras cada una)
   - Deben justificar la oportunidad comercial

3. ¿CÓMO VENDER?
   - **LEAD WITH:** ¿Con qué empezar la conversación?
     Ejemplo: "Ahorrar tiempo del personal automatizando conversaciones repetitivas"
     NO: "Inteligencia Artificial"
   
   - **MAIN BUSINESS BENEFIT:** Beneficio principal en términos de negocio
     Ejemplo: "Aumentar reservas sin contratar más personal"
     NO: "Mejorar experiencia del cliente" (muy genérico)
   
   - **COMMUNICATION STYLE:** Recomendación completa
     Ejemplo: "Profesional, amigable y consultivo. Enfocarse en resolver problemas de negocio antes de hablar de tecnología."
     NO: "Casual"
   
   - **DECISION MAKER:** Quién toma decisiones

4. FORTALEZAS DEL NEGOCIO
   - Cada fortaleza DEBE explicar cómo ayuda a la venta
   - Conectar fortaleza → oportunidad comercial

RESPONDE EN JSON:
{{
    "primary_service": "Servicio a vender",
    "secondary_service": "Servicio secundario o null",
    "estimated_opportunity": "Low|Medium|High",
    "why_this_service": [
        "Justificación 1 del servicio",
        "Justificación 2 del servicio",
        "Justificación 3 del servicio"
    ],
    "why_this_company": [
        "Razón 1 (máx 10 palabras)",
        "Razón 2 (máx 10 palabras)",
        "Razón 3 (máx 10 palabras)"
    ],
    "lead_with": "Con qué empezar la conversación (específico, no genérico)",
    "main_business_benefit": "Beneficio principal en términos de negocio",
    "communication_style": "Recomendación completa de estilo (no solo tono)",
    "decision_maker": "Quién toma decisiones",
    "commercial_opportunities": [
        {{
            "description": "Potencial para [acción específica]"
        }}
    ],
    "business_strengths": [
        {{
            "strength": "Fortaleza específica",
            "opportunity": "Cómo esto ayuda a cerrar la venta"
        }}
    ],
    "estimated_success_probability": 75
}}
"""
        return prompt
