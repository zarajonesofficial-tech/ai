import sys
import logging
from loguru import logger

def setup_logging(debug=True):
    """
    Configures a clean, organized, and color-coded logging system.
    """
    # 1. Remove default handlers
    logger.remove()
    logging.getLogger("uvicorn").handlers = []
    logging.getLogger("uvicorn.access").handlers = []
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("discord").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    # 2. Define custom format
    # Example: 2026-05-08 02:20:00 | CORE   | App starting...
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{extra[module]}</cyan> | "
        "<level>{message}</level>"
    )

    # 3. Add console handler
    logger.configure(extra={"module": "APP"}) # Default module
    logger.add(
        sys.stdout,
        format=log_format,
        level="DEBUG" if debug else "INFO",
        colorize=True
    )

    return logger

# Create pre-configured scoped loggers
core_logger = logger.bind(module="CORE")
bot_logger = logger.bind(module="BOT")
ai_logger = logger.bind(module="AI")
worker_logger = logger.bind(module="WORKER")
mcp_logger = logger.bind(module="MCP")
