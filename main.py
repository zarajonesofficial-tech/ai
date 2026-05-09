import asyncio
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from core.config import settings
from utils.logger import setup_logging, core_logger

# Initialize Logging
setup_logging(debug=settings.DEBUG)

from mcp_server.server import mcp_app
from api.routers.dashboard import router as dashboard_router
from api.routers.state import router as state_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    core_logger.info(f"Starting {settings.PROJECT_NAME}...")
    
    # Start Discord Bot
    from bot.main import start_bot
    asyncio.create_task(start_bot())
    
    # Start Autonomous Workflows
    from core.workflows import start_workflows
    asyncio.create_task(start_workflows())
    
    yield
    
    # Shutdown logic
    core_logger.info(f"Shutting down {settings.PROJECT_NAME}...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-powered operations, automation, and community management platform.",
    version="0.1.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount MCP Server
app.mount("/mcp", mcp_app.sse_app(mount_path="/mcp"))

# Mount Static Files for Dashboard
app.mount("/css", StaticFiles(directory="frontend/css"), name="frontend-css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="frontend-js")

# Include API Routers
app.include_router(state_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "project": settings.PROJECT_NAME}

@app.get("/dashboard")
async def dashboard_page():
    return FileResponse("frontend/index.html")

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

if __name__ == "__main__":
    import uvicorn
    # Use environment port for Railway/Production, fallback to 8001
    port = int(os.getenv("PORT", 8001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
