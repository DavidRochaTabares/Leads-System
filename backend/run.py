import asyncio
import sys
from dotenv import load_dotenv

# Load .env file before anything else
load_dotenv()

# Fix for Playwright on Windows - use SelectorEventLoop instead of ProactorEventLoop
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "__main__":
    import uvicorn
    # Disable reload on Windows to maintain event loop policy
    reload = False if sys.platform == 'win32' else True
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=reload)
