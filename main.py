import asyncio
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from utils.logger import setup_logging, core_logger

# Initialize Logging
setup_logging(debug=settings.DEBUG)

from mcp_server.server import mcp_app
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

# Include API Routers
app.include_router(state_router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "project": settings.PROJECT_NAME}

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API. Open frontend/index.html to view the dashboard."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
