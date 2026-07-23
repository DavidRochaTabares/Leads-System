import time
from typing import List, Dict, Any
from repositories.prospecting_supabase_repository import ProspectingSupabaseRepository
from repositories.company_repository import CompanyRepository
from services.supabase_client import get_supabase
from services.ai_service import AIService


def execute_ai_analysis_sync(session_id: str) -> None:
    """
    Synchronous AI Analysis Worker - Runs AFTER scraping completes.
    
    Analyzes each company using AI to generate:
    - Business insights
    - Sales strategy
    - Personalized outreach content
    - Lead scoring
    
    This worker does NOT scrape. It only analyzes existing data.
    """
    print(f"[AI WORKER] Starting AI analysis for session {session_id}")
    
    supabase = get_supabase()
    session_repo = ProspectingSupabaseRepository(supabase)
    company_repo = CompanyRepository(supabase)
    
    try:
        # Get session data
        session = session_repo.get_by_id(session_id)
        if not session:
            raise Exception("Session not found")
        
        industry = session['industry']
        location = session['location']
        
        # Get all companies for this session
        companies = company_repo.get_companies_by_session(session_id)
        
        if not companies:
            session_repo.add_log(session_id, "No companies to analyze")
            return
        
        # Change status to 'analyzing'
        total_companies = len(companies)
        session_repo.update_status(session_id, "analyzing", progress=0)
        session_repo.add_log(session_id, f"Starting AI analysis for {total_companies} companies")
        
        # Initialize AI service
        # Options: "openai" (GPT-4o-mini) or "claude" (Claude Sonnet)
        try:
            ai_service = AIService(provider="openai")
            session_repo.add_log(session_id, "AI service initialized successfully")
        except Exception as e:
            session_repo.add_log(session_id, f"Failed to initialize AI service: {str(e)}", level="error")
            raise
        
        analyzed_count = 0
        failed_count = 0
        
        for company in companies:
            company_name = company.get('name', 'Unknown')
            
            # Skip if already analyzed
            if company.get('ai_analyzed_at'):
                session_repo.add_log(session_id, f"Already analyzed: {company_name}")
                analyzed_count += 1
                # Update progress even for skipped companies
                progress = int((analyzed_count / total_companies) * 100)
                session_repo.update_status(session_id, "analyzing", progress=progress)
                continue
            
            try:
                session_repo.add_log(session_id, f"Analyzing: {company_name}")
                
                # Prepare company data for AI
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
                
                session_repo.add_log(session_id, f"Calling AI API for {company_name}...")
                
                # Call AI service (synchronous)
                ai_analysis = ai_service.analyze_company(company_data)
                
                session_repo.add_log(session_id, f"AI response received for {company_name}")
                
                # Store AI analysis
                company_repo.update_ai_analysis(company['id'], ai_analysis)
                
                analyzed_count += 1
                session_repo.add_log(session_id, f"AI analysis saved: {company_name}")
                
                # Update progress
                progress = int((analyzed_count / total_companies) * 100)
                session_repo.update_status(session_id, "analyzing", progress=progress)
                
                # Small delay to avoid rate limiting
                time.sleep(1)
            
            except Exception as e:
                failed_count += 1
                import traceback
                error_trace = traceback.format_exc()
                session_repo.add_log(
                    session_id,
                    f"AI analysis failed for {company_name}: {str(e)}",
                    level="error"
                )
                session_repo.add_log(
                    session_id,
                    f"Error trace: {error_trace[:500]}",
                    level="error"
                )
                # Continue with next company
                continue
        
        # Summary
        session_repo.add_log(
            session_id,
            f"AI analysis complete: {analyzed_count} analyzed, {failed_count} failed"
        )
        
        # Mark session as completed with AI analysis
        session_repo.update_status(session_id, "completed", progress=100)
        
        print(f"[AI WORKER] Completed AI analysis for session {session_id}")
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"[AI WORKER ERROR] {error_details}")
        session_repo.add_log(session_id, f"AI worker failed: {str(e)}", level="error")
