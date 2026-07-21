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
        
        prompt = f"""You are a Senior Digital Transformation Consultant at SpineDev.

Your job is to analyze this company and identify REAL business opportunities.

Be honest. Never invent problems. Only recommend services that genuinely create value.

COMPANY INFORMATION:
- Name: {name}
- Industry: {industry}
- Location: {location}
- Website: {website}
- Phone: {phone}
- Address: {address}
- Google Rating: {rating} ({review_count} reviews)
- Emails found: {', '.join(emails) if emails else 'None'}
- Social Media: {social_text}
- Website Features: {features_text}
- Rule-based Recommendations: {', '.join(recommended_services) if recommended_services else 'None'}

ANALYSIS REQUIREMENTS:

1. WEBSITE ASSESSMENT
   - Evaluate based on available data
   - Only recommend redesign if truly justified
   - Consider: professionalism, trust signals, modern vs outdated

2. BRANDING ASSESSMENT
   - Evaluate digital presence consistency
   - Social media activity
   - Professional image

3. PAIN POINTS
   - Identify REAL problems based on data
   - Never invent issues
   - Focus on measurable gaps

4. BUSINESS OPPORTUNITIES
   - What specific value can SpineDev provide?
   - Why would this company benefit?
   - Business reasoning required

5. RECOMMENDED SERVICES
   - Only recommend if justified
   - Explain WHY each service fits
   - Think like a consultant, not a salesperson

6. LEAD SCORE (0-100)
   - Based on: digital maturity, business size, growth potential
   - Explain your reasoning

7. SALES STRATEGY
   - How to approach this specific company
   - What angle to use
   - Key value propositions

8. OUTREACH CONTENT
   - Personalized cold email (professional, value-focused)
   - LinkedIn message (concise, relevant)
   - WhatsApp message (brief, friendly)
   - Cold call script (structured, natural)

9. OBJECTION HANDLING
   - Likely objections from this company
   - How to address them

10. NEXT BEST ACTION
    - Immediate next step for sales team

Return ONLY valid JSON with this exact structure:
{{
  "summary": "2-3 sentence executive summary",
  "website_assessment": "Honest evaluation of their website",
  "branding_assessment": "Evaluation of their brand presence",
  "pain_points": ["pain point 1", "pain point 2", ...],
  "business_opportunities": ["opportunity 1", "opportunity 2", ...],
  "recommended_services": [
    {{"service": "Service Name", "justification": "Why this fits"}}
  ],
  "lead_score": 75,
  "score_reason": "Explanation of the score",
  "sales_strategy": "How to approach this company",
  "personalized_email": "Full email text",
  "linkedin_message": "LinkedIn message text",
  "whatsapp_message": "WhatsApp message text",
  "cold_call_script": "Call script with structure",
  "possible_objections": ["objection 1", "objection 2", ...],
  "next_best_action": "Immediate next step"
}}

Return ONLY the JSON. No markdown, no explanation."""

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
            result = json.loads(content)
            return result
        
        except Exception as e:
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
