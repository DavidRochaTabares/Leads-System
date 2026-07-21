import asyncio
import sys
from dotenv import load_dotenv

# Load .env file before anything else
load_dotenv()

# Fix for Playwright on Windows - must be set before uvicorn starts
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
