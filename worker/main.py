import asyncio
from playwright.async_api import async_playwright
from utils.supabase_client import supabase
from core.config import settings
from utils.logger import setup_logging, worker_logger
import json
import signal

# Initialize Logging
setup_logging(debug=settings.DEBUG)

async def run_panel_restart(page):
    """
    Example automation workflow: Login and click restart.
    """
    worker_logger.info(f"Navigating to {settings.PANEL_URL}...")
    await page.goto(settings.PANEL_URL)
    
    # Example selectors (must be adjusted for the actual panel)
    await page.fill('input[name="username"]', settings.PANEL_USER)
    await page.fill('input[name="password"]', settings.PANEL_PASS)
    await page.click('button[type="submit"]')
    
    await page.wait_for_load_state("networkidle")
    worker_logger.info("Login successful. Attempting restart...")
    
    # Click restart button
    await page.click('button#restart-btn')
    await page.wait_for_timeout(5000) # Wait for trigger
    return {"status": "success", "message": "Restart command sent via Playwright"}

async def process_jobs():
    worker_logger.info("Automation Worker started. Polling for jobs...")
    
    # Graceful shutdown handler
    stop_event = asyncio.Event()
    
    def signal_handler():
        worker_logger.info("Shutdown signal received...")
        stop_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        
        while not stop_event.is_set():
            try:
                # 1. Poll for pending jobs
                response = supabase.table("automation_jobs").select("*").eq("status", "pending").limit(1).execute()
                jobs = response.data
                
                if jobs:
                    job = jobs[0]
                    job_id = job["id"]
                    task_type = job["task_type"]
                    
                    worker_logger.info(f"Processing job {job_id}: {task_type}")
                    supabase.table("automation_jobs").update({"status": "running"}).eq("id", job_id).execute()
                    
                    page = await context.new_page()
                    result = {}
                    
                    try:
                        if task_type == "panel_restart":
                            result = await run_panel_restart(page)
                        else:
                            result = {"error": f"Unknown task type: {task_type}"}
                        
                        supabase.table("automation_jobs").update({
                            "status": "completed", 
                            "result": result
                        }).eq("id", job_id).execute()
                        worker_logger.info(f"Job {job_id} completed.")
                        
                    except Exception as e:
                        worker_logger.error(f"Job {job_id} failed: {e}")
                        supabase.table("automation_jobs").update({
                            "status": "failed", 
                            "result": {"error": str(e)}
                        }).eq("id", job_id).execute()
                    
                    await page.close()
                
                # Check for stop every second during the interval
                for _ in range(10):
                    if stop_event.is_set(): break
                    await asyncio.sleep(1)
                
            except Exception as e:
                worker_logger.error(f"Worker loop error: {e}")
                await asyncio.sleep(30) # Backoff
        
        try:
            worker_logger.info("Closing browser context...")
            await browser.close()
        except Exception:
            # Ignore connection closed errors during shutdown
            pass
            
        worker_logger.info("Worker stopped.")

if __name__ == "__main__":
    asyncio.run(process_jobs())
