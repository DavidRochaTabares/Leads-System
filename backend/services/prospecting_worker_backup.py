import asyncio
from concurrent.futures import ThreadPoolExecutor
from repositories.prospecting_supabase_repository import ProspectingSupabaseRepository
from repositories.company_repository import CompanyRepository
from services.supabase_client import get_supabase
from services.google_maps_miner_sync import GoogleMapsMinerSync
from services.website_scraper import WebsiteScraper
from services.ai_analysis_worker import execute_ai_analysis
from config.mining_config import *


async def execute_prospecting_session(session_id: str) -> None:
    print(f"[WORKER] Starting worker for session {session_id}")
    supabase = get_supabase()
    session_repo = ProspectingSupabaseRepository(supabase)
    company_repo = CompanyRepository(supabase)
    miner = None
    
    try:
        print(f"[WORKER] Updating status to running")
        session_repo.update_status(session_id, "running", progress=0)
        session_repo.add_log(session_id, "Worker started")
        print(f"[WORKER] Worker started log added")
        
        # Get session details
        session = session_repo.get_by_id(session_id)
        if not session:
            raise Exception("Session not found")
        
        industry = session['industry']
        location = session['location']
        max_companies = session['max_companies']
        
        # Initialize browser
        session_repo.add_log(session_id, "Opening Google Maps")
        miner = GoogleMapsMinerSync()
        
        # Run in thread pool to avoid event loop issues
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(max_workers=1)
        
        await loop.run_in_executor(executor, miner.initialize)
        
        # Search
        session_repo.add_log(session_id, f"Searching: {industry} in {location}")
        await loop.run_in_executor(executor, miner.search, industry, location)
        session_repo.add_log(session_id, "Search completed")
        
        # Create website scraper once (reuses browser)
        scraper = WebsiteScraper(miner.page)
        
        # Mining loop
        companies_saved = 0
        seen_urls = set()
        scroll_attempts_without_new = 0
        
        while companies_saved < max_companies:
            cards = await loop.run_in_executor(executor, miner.get_business_cards)
            
            if not cards:
                session_repo.add_log(session_id, "No businesses found")
                break
            
            new_cards_found = False
            
            for card in cards:
                if companies_saved >= max_companies:
                    break
                
                # Click and extract
                clicked = await loop.run_in_executor(executor, miner.click_business_card, card)
                if not clicked:
                    continue
                
                data = await loop.run_in_executor(executor, miner.extract_business_data)
                
                if not data or not data.get('google_maps_url'):
                    continue
                
                # Check if already processed
                if data['google_maps_url'] in seen_urls:
                    continue
                
                seen_urls.add(data['google_maps_url'])
                new_cards_found = True
                
                # Check duplicate in database
                if company_repo.is_duplicate(session_id, data['google_maps_url']):
                    session_repo.add_log(session_id, f"Duplicate skipped: {data['name']}")
                    continue
                
                # Save company
                try:
                    company = company_repo.create_company(
                        session_id=session_id,
                        name=data['name'],
                        google_maps_url=data['google_maps_url'],
                        website=data.get('website'),
                        phone=data.get('phone'),
                        address=data.get('address'),
                        rating=data.get('rating'),
                        review_count=data.get('review_count')
                    )
                    companies_saved += 1
                    session_repo.add_log(session_id, f"Saved: {data['name']}")
                    
                    # Scrape website if available
                    if data.get('website'):
                        try:
                            session_repo.add_log(session_id, f"Scraping website: {data['name']}")
                            website_data = await loop.run_in_executor(
                                executor, 
                                scraper.scrape, 
                                data['website']
                            )
                            company_repo.update_website_data(company['id'], website_data)
                            session_repo.add_log(session_id, f"Website scraped: {data['name']}")
                        except Exception as e:
                            session_repo.add_log(session_id, f"Website scrape failed for {data['name']}: {str(e)}", level="error")
                    
                    # Update progress
                    if companies_saved % PROGRESS_UPDATE_EVERY_N_COMPANIES == 0:
                        progress = int((companies_saved / max_companies) * 100)
                        session_repo.update_status(session_id, "running", progress=progress)
                except Exception as e:
                    session_repo.add_log(session_id, f"Failed to save {data['name']}: {str(e)}", level="error")
            
            # Scroll for more results
            if companies_saved < max_companies:
                await loop.run_in_executor(executor, miner.scroll_results_panel)
                
                if not new_cards_found:
                    scroll_attempts_without_new += 1
                    if scroll_attempts_without_new >= MAX_SCROLL_ATTEMPTS_WITHOUT_NEW_RESULTS:
                        session_repo.add_log(session_id, "No more results available")
                        break
                else:
                    scroll_attempts_without_new = 0
        
        # Scraping complete - now start AI analysis
        session_repo.add_log(session_id, f"Mining completed. Total companies: {companies_saved}")
        session_repo.update_status(session_id, "completed", progress=100)
        session_repo.add_log(session_id, "Mining phase completed. Starting AI analysis...")
        
        # Run AI analysis worker (it will handle status updates)
        await execute_ai_analysis(session_id)
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"[WORKER ERROR] {error_details}")
        session_repo.update_status(session_id, "failed")
        session_repo.add_log(session_id, f"Worker failed: {str(e)}", level="error")
        session_repo.add_log(session_id, f"Error details: {error_details[:500]}", level="error")
    finally:
        if miner:
            try:
                # Close browser
                miner.close()
            except Exception as e:
                print(f"[WORKER] Browser close warning: {str(e)}")
