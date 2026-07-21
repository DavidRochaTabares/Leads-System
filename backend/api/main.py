import logging
import traceback
import asyncio
import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core.config import settings
from api.routes import health, auth, prospecting

# Fix for Playwright on Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SpineDev Platform API",
    description="Internal operating platform for SpineDev",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

logger.info(f"CORS origins configured: {settings.cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "message": str(exc)},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(prospecting.router)


@app.get("/")
async def root():
    return {
        "message": "SpineDev Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }
