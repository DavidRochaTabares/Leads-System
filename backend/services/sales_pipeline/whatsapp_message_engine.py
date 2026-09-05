import os
import json
from typing import Dict, Any
from datetime import datetime
from openai import OpenAI


class WhatsAppMessageEngine:
    """
    WhatsApp Message Engine - Independent AI Module
    
    Responsibility: Generate personalized WhatsApp messages for B2B sales
    
    Input: Sales Brief + Company Info
    Output: Natural, conversational WhatsApp message
    
    Rules:
    - Spanish only
    - Natural and human
    - Never mention AI, analysis, or Google Maps
    - 80-150 words
    - Focus on business problem
    - Conversational, not aggressive
    """
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        self.client = OpenAI(api_key=api_key)
    
    def generate_message(self, company_data: Dict[str, Any], sales_brief: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized WhatsApp message
        
        Args:
            company_data: {
                'name': str,
                'industry': str,
                'location': str,
        
        Returns:
            {
                'template_name': str,
                'variables': [str, str, str],
                'preview': str (full message preview),
                'version': int,
                'generated_at': str (ISO timestamp)
            }
        """
        print(f"[WHATSAPP ENGINE] Generating template variables for {company_data.get('name')}")
        
        # Generate the 3 template variables
        variables = self.generate_template_variables(company_data, sales_brief)
        
        # Build preview of how the message will look
        template_name = "cold_outreach_v2"
        preview = f"""Hola,

{variables[0]}

{variables[1]}

En SpineDev ayudamos a empresas a {variables[2]}.

¿Tendrías 15 minutos para una llamada esta semana?"""
        
        print(f"[WHATSAPP ENGINE] Template variables generated successfully")
        
        return {
            'template_name': template_name,
            'variables': variables,
            'preview': preview,
            'version': 1,
            'generated_at': datetime.utcnow().isoformat() + 'Z'
        }
    
    def regenerate_message(
        self, 
        company_data: Dict[str, Any], 
        sales_brief: Dict[str, Any],
        current_version: int = 1
    ) -> Dict[str, Any]:
        """
        Regenerate template variables with increased version number
        """
        print(f"[WHATSAPP ENGINE] Regenerating template variables (version {current_version + 1})")
        
        result = self.generate_message(company_data, sales_brief)
        result['version'] = current_version + 1
        
        return result
    
    def _build_message_prompt(self, company_data: Dict[str, Any], sales_brief: Dict[str, Any]) -> str:
        """Build the message generation prompt"""
        
        name = company_data.get('name', 'la empresa')
        industry = company_data.get('industry', 'No especificado')
        website = company_data.get('website', '')
        
        # Extract Sales Brief
        primary_service = sales_brief.get('primary_service', 'servicios digitales')
        why_company = sales_brief.get('why_this_company', [])
        lead_with = sales_brief.get('lead_with', '')
        main_benefit = sales_brief.get('main_business_benefit', '')
        decision_maker = sales_brief.get('decision_maker', 'dueño/gerente')
        comm_style = sales_brief.get('communication_style', 'profesional y amigable')
        
        prompt = f"""
Eres un vendedor B2B experimentado escribiendo un mensaje de WhatsApp.

OBJETIVO: Iniciar una conversación. NO vender. Una respuesta = éxito.

=== SALES BRIEF ===

EMPRESA: {name}
SITIO WEB: {website}
INDUSTRIA: {industry}

OBSERVACIONES REALES (de aquí salen tus observaciones):
{chr(10).join(f"- {reason}" for reason in why_company[:3])}

ÁNGULO DE CONVERSACIÓN:
{lead_with}

RESULTADO DE NEGOCIO:
{main_benefit}

SERVICIO: {primary_service}

=== ESTRUCTURA (NUNCA CAMBIES ESTE ORDEN) ===

1. SALUDO
   - "Hola" o "Buen día" (sin nombre si es genérico como "Resultados")
   - Si el nombre es claro, úsalo

2. UNA OBSERVACIÓN REAL
   - Toma UNA observación de "OBSERVACIONES REALES"
   - Escríbela de forma natural, NO digas "vi", "noté", "analicé"
   - Escribe como si estuvieras describiendo algo que observaste
   
   BIEN: "Actualmente parece que la mayoría de consultas se manejan por WhatsApp..."
   BIEN: "El sitio web no tiene un sistema para capturar leads..."
   MAL: "Vi una gran oportunidad de crecimiento."
   MAL: "Noté que tienen potencial digital."

3. CONSECUENCIA DE NEGOCIO
   - Explica qué problema causa esa observación
   - Sé específico, NO genérico
   
   BIEN: "Esto suele hacer que se pierdan consultas cuando el equipo está ocupado."
   BIEN: "Muchas veces significa que clientes potenciales no pueden agendar fuera de horario."
   MAL: "Esto puede mejorar tu negocio."
   MAL: "Hay oportunidad de crecer."

4. SPINEDEV (UNA SOLA FRASE)
   - Menciona SpineDev SOLO UNA VEZ
   - Enfócate en el RESULTADO, no en el servicio
   - 80% del mensaje es sobre el cliente, 20% sobre SpineDev
   
   BIEN: "Ayudamos a empresas a responder más consultas sin aumentar personal."
   BIEN: "Podemos ayudarte a que más clientes agenden automáticamente."
   MAL: "Ofrecemos automatización con IA."
   MAL: "Desarrollamos soluciones digitales."

5. CTA NATURAL
   - Conecta el CTA con el problema específico mencionado
   - Sin presión, conversacional
   
   BIEN: "Si esto es algo que están enfrentando, ¿te parecería bien una llamada de 15 minutos?"
   BIEN: "¿Tendrías tiempo esta semana para una llamada rápida sobre esto?"
   MAL: "¡Agenda ahora!"
   MAL: "No pierdas esta oportunidad."

=== FRASES PROHIBIDAS ===

❌ "Vi/Noté/Analicé una oportunidad"
❌ "Tienen potencial/gran potencial"
❌ "Ayudamos a crecer negocios"
❌ "Mejorar presencia digital"
❌ "Aumentar visibilidad"
❌ "Soluciones modernas/digitales"
❌ "Transformación digital"
❌ "Inteligencia Artificial/IA"
❌ "Herramientas/tecnología"

=== REGLAS ===

✓ 60-120 palabras
✓ Cada observación viene del Sales Brief (NUNCA inventes)
✓ 80% sobre el cliente, 20% sobre SpineDev
✓ SpineDev mencionado SOLO UNA VEZ
✓ Vende el RESULTADO, no el servicio
✓ Suena como persona real, NO como ChatGPT
✓ Objetivo: GANAR UNA RESPUESTA

=== VERIFICACIÓN ANTES DE RESPONDER ===

Verifica:
✓ ¿La observación está en "OBSERVACIONES REALES"?
✓ ¿Evité frases prohibidas?
✓ ¿SpineDev mencionado solo una vez?
✓ ¿80% sobre el cliente, 20% sobre SpineDev?
✓ ¿El CTA conecta con el problema mencionado?
✓ ¿Suena como si lo escribió una persona real?

Si alguna respuesta es NO, reescribe.

ESCRIBE EL MENSAJE (60-120 palabras):
"""
        return prompt
    
    def generate_template_variables(self, company_data: Dict[str, Any], sales_brief: Dict[str, Any]) -> list:
        """
        Generate 3 personalized variables for WhatsApp template using AI
        
        Template structure:
        Hola,
        {{1}}  <-- Observación específica
        {{2}}  <-- Impacto de negocio
        En SpineDev ayudamos a empresas a {{3}}.  <-- Beneficio específico
        ¿Tendrías 15 minutos para una llamada esta semana?
        
        Returns:
            List of 3 strings [observation, impact, benefit]
        """
        print(f"[WHATSAPP ENGINE] Generating template variables for {company_data.get('name')}")
        
        # Extract Sales Brief data
        name = company_data.get('name', 'la empresa')
        website = company_data.get('website', 'N/A')
        industry = company_data.get('industry', 'N/A')
        why_company = sales_brief.get('why_this_company', [])
        lead_with = sales_brief.get('lead_with', '')
        main_benefit = sales_brief.get('main_business_benefit', '')
        primary_service = sales_brief.get('primary_service', 'automatización')
        
        # Build AI prompt for generating 3 personalized variables
        prompt = f"""
Genera 3 variables personalizadas para un mensaje de WhatsApp B2B amigable y conversacional.

EMPRESA: {name}
SITIO WEB: {website}
INDUSTRIA: {industry}
OBSERVACIONES DEL SALES BRIEF:
{chr(10).join(f"- {reason}" for reason in why_company[:3])}
ÁNGULO PRINCIPAL:
{lead_with}
BENEFICIO PRINCIPAL:
{main_benefit}
SERVICIO: {primary_service}

CONTEXTO DEL TEMPLATE:
El mensaje completo será:
"Hola,
{{{{1}}}}
{{{{2}}}}
En SpineDev ayudamos a empresas a {{{{3}}}}.
¿Tendrías 15 minutos para una llamada esta semana?"

TAREA:
Genera 3 variables separadas por "|||":

VARIABLE 1 (Introducción + Observación): 
- Presenta por qué escribes de forma amigable
- Menciona la observación específica
- Tono: conversacional, como si conocieras a la persona
- Máx 200 caracteres

VARIABLE 2 (Impacto de Negocio):
- Explica el problema que causa esa observación
- Conecta con el negocio del cliente
- Tono: empático, no alarmista
- Máx 200 caracteres

VARIABLE 3 (Beneficio Específico):
- Cómo ayudamos específicamente (verbo en infinitivo)
- Debe completar: "En SpineDev ayudamos a empresas a..."
- Específico al problema mencionado
- Máx 150 caracteres

FORMATO DE RESPUESTA:
Variable 1|||Variable 2|||Variable 3

EJEMPLO BUENO:
Estuve revisando {name} y noté que la mayoría de consultas se manejan por WhatsApp|||Esto suele hacer que se pierdan oportunidades cuando el equipo está ocupado atendiendo otras consultas|||responder automáticamente a clientes 24/7 sin aumentar personal

EJEMPLO MALO:
Presencia digital limitada|||Pérdida de clientes|||mejorar presencia digital

REGLAS:
✓ Variable 1: Amigable, da contexto de por qué escribes
✓ Variable 2: Empático, muestra que entiendes el problema
✓ Variable 3: Específico, verbo infinitivo, sin mencionar SpineDev
✓ TODO: Natural, conversacional, como un vendedor experimentado
✓ NO uses: "optimizar", "potencial", "transformación digital"

GENERA LAS 3 VARIABLES:
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un vendedor B2B experimentado. Escribes observaciones específicas y naturales sobre empresas."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            result = response.choices[0].message.content.strip()
            
            # Parse the 3 variables
            parts = result.split('|||')
            
            if len(parts) >= 3:
                observation = parts[0].strip().strip('"').strip("'")
                impact = parts[1].strip().strip('"').strip("'")
                benefit = parts[2].strip().strip('"').strip("'")
                
                # Clean variables: remove newlines, tabs, and excessive spaces
                # WhatsApp doesn't allow these in template variables
                import re
                observation = re.sub(r'[\n\r\t]+', ' ', observation)  # Replace newlines/tabs with space
                observation = re.sub(r'\s{2,}', ' ', observation)     # Replace multiple spaces with single space
                
                impact = re.sub(r'[\n\r\t]+', ' ', impact)
                impact = re.sub(r'\s{2,}', ' ', impact)
                
                benefit = re.sub(r'[\n\r\t]+', ' ', benefit)
                benefit = re.sub(r'\s{2,}', ' ', benefit)
                
                # Ensure length limits
                observation = observation[:200].strip()
                impact = impact[:200].strip()
                benefit = benefit[:150].strip()
                
                variables = [observation, impact, benefit]
                
                print(f"[WHATSAPP ENGINE] Variables generated:")
                print(f"  1. {observation}")
                print(f"  2. {impact}")
                print(f"  3. {benefit}")
                
                return variables
            else:
                raise Exception("AI did not return 3 variables")
            
        except Exception as e:
            print(f"[WHATSAPP ENGINE ERROR] Failed to generate template variables: {str(e)}")
            # Fallback
            observation = lead_with if lead_with else (why_company[0] if why_company else "Notamos que tu empresa podría mejorar la atención al cliente")
            impact = "Esto puede afectar la satisfacción de tus clientes"
            benefit = "mejorar la experiencia del cliente"
            return [observation[:150], impact[:150], benefit[:100]]
