import os
import sys
import json
import traceback
from dotenv import load_dotenv
from services.supabase_client import get_supabase
from services.ai_service import AIService

# Load .env file
load_dotenv()

print("=" * 80)
print("AI ANALYSIS DIAGNOSTIC TEST")
print("=" * 80)

# Get one company from database
supabase = get_supabase()

print("\n[1] Fetching company from database...")
response = supabase.table("companies").select("*").limit(1).execute()

if not response.data or len(response.data) == 0:
    print("ERROR: No companies found in database")
    sys.exit(1)

company = response.data[0]
print(f"✓ Company loaded: {company.get('name', 'Unknown')}")

# Get session data for industry/location
session_id = company.get('session_id')
session_response = supabase.table("prospecting_sessions").select("*").eq("id", session_id).execute()
session = session_response.data[0] if session_response.data else {}

industry = session.get('industry', 'Unknown')
location = session.get('location', 'Unknown')

print(f"  Industry: {industry}")
print(f"  Location: {location}")

# Prepare company data (EXACT same as AI Worker)
company_data = {
    'name': company.get('name'),
    'industry': industry,
    'location': location,
    'website': company.get('website'),
    'phone': company.get('phone'),
    'address': company.get('address'),
    'rating': company.get('rating'),
    'review_count': company.get('review_count'),
    'emails': company.get('emails', []),
    'social_links': company.get('social_links', {}),
    'features': company.get('features', {}),
    'recommended_services': company.get('recommended_services', [])
}

print("\n[2] Company data prepared:")
print(f"  - Name: {company_data['name']}")
print(f"  - Website: {company_data['website']}")
print(f"  - Emails: {len(company_data['emails'])} found")
print(f"  - Social links: {len(company_data['social_links'])} found")
print(f"  - Features: {sum(1 for v in company_data['features'].values() if v)} detected")

# Initialize AI service (EXACT same as AI Worker)
print("\n[3] Initializing AI service...")
try:
    ai_service = AIService(provider="openai")
    print(f"✓ AI Service initialized")
    print(f"  Provider: openai")
    print(f"  Model: {ai_service.model}")
except Exception as e:
    print(f"ERROR initializing AI service: {e}")
    traceback.print_exc()
    sys.exit(1)

# Build prompt (EXACT same method as AIService)
print("\n[4] Building prompt...")
prompt = ai_service._build_analysis_prompt(company_data)

# Estimate tokens (rough: 1 token ≈ 4 characters)
prompt_chars = len(prompt)
estimated_tokens = prompt_chars // 4

print(f"✓ Prompt built")
print(f"  Characters: {prompt_chars:,}")
print(f"  Estimated input tokens: {estimated_tokens:,}")
print(f"  Screenshots: 0 (not implemented yet)")

# Show first 500 chars of prompt
print("\n[5] Prompt preview (first 500 chars):")
print("-" * 80)
print(prompt[:500])
print("...")
print("-" * 80)

# Make API call
print("\n[6] Calling OpenAI API...")
print(f"  Model: {ai_service.model}")
print(f"  Max tokens: 4000")
print(f"  Temperature: 0.7")
print(f"  Response format: json_object")
print()

try:
    # EXACT same call as AIService._call_openai
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model=ai_service.model,
        messages=[{
            "role": "system",
            "content": "You are a Senior Digital Transformation Consultant. Return only valid JSON."
        }, {
            "role": "user",
            "content": prompt
        }],
        temperature=0.7,
        max_tokens=4000,
        response_format={"type": "json_object"}
    )
    
    print("=" * 80)
    print("SUCCESS!")
    print("=" * 80)
    
    # Extract response
    content = response.choices[0].message.content
    result = json.loads(content)
    
    print(f"\nResponse received:")
    print(f"  Request ID: {response.id}")
    print(f"  Model used: {response.model}")
    print(f"  Finish reason: {response.choices[0].finish_reason}")
    print(f"  Input tokens: {response.usage.prompt_tokens:,}")
    print(f"  Output tokens: {response.usage.completion_tokens:,}")
    print(f"  Total tokens: {response.usage.total_tokens:,}")
    
    # Save to file
    output_file = "test_ai_output.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Analysis saved to: {output_file}")
    
    print("\n" + "=" * 80)
    print("DIAGNOSTIC COMPLETE - AI ANALYSIS WORKS!")
    print("=" * 80)

except Exception as e:
    print("=" * 80)
    print("FAILURE!")
    print("=" * 80)
    
    print(f"\nException type: {type(e).__name__}")
    print(f"Exception message: {str(e)}")
    
    # Try to extract OpenAI error details
    if hasattr(e, 'status_code'):
        print(f"\nStatus code: {e.status_code}")
    
    if hasattr(e, 'response'):
        print(f"\nResponse body: {e.response}")
    
    if hasattr(e, 'request_id'):
        print(f"\nRequest ID: {e.request_id}")
    
    print("\n" + "=" * 80)
    print("FULL TRACEBACK:")
    print("=" * 80)
    traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("DIAGNOSTIC COMPLETE - AI ANALYSIS FAILED")
    print("=" * 80)
    
    sys.exit(1)
