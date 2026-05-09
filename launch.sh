#!/bin/bash

set -u

# CHRIZ__3656 AI - Unified Launch Script

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

require_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        log_error "Required command not found: $1"
        exit 1
    fi
}

install_python_requirements() {
    log_info "Checking Python dependencies..."
    if ! python - <<'PY' >/dev/null 2>&1
import importlib.util
import sys

modules = [
    "fastapi",
    "uvicorn",
    "discord",
    "pydantic_settings",
    "supabase",
    "playwright",
    "boto3",
    "aioboto3",
    "httpx",
    "multipart",
    "dotenv",
    "mcp",
    "aiorcon",
    "loguru",
    "jose",
    "passlib",
]

missing = [name for name in modules if importlib.util.find_spec(name) is None]
sys.exit(1 if missing else 0)
PY
    then
        log_warn "Missing Python packages detected. Installing from requirements.txt..."
        python -m pip install -r requirements.txt || {
            log_error "Failed to install Python dependencies."
            exit 1
        }
    else
        log_info "Python dependencies already available."
    fi
}

install_playwright_browser() {
    log_info "Checking Playwright Chromium..."
    if ! python - <<'PY' >/dev/null 2>&1
from pathlib import Path
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    executable = Path(p.chromium.executable_path)
    if not executable.exists():
        raise SystemExit(1)
PY
    then
        log_warn "Playwright Chromium is missing. Installing..."
        python -m playwright install chromium || {
            log_error "Failed to install Playwright Chromium."
            exit 1
        }
    else
        log_info "Playwright Chromium already available."
    fi
}

cleanup() {
    echo -e "\n${RED}[SHUTDOWN]${NC} Stopping all services..."
    jobs -p | xargs -r kill
    exit
}

echo -e "${CYAN}=============================================${NC}"
echo -e "${CYAN}      CHRIZ__3656 AI PLATFORM LAUNCHER      ${NC}"
echo -e "${CYAN}=============================================${NC}"

require_command python3

if [ -d "venv" ]; then
    log_info "Activating virtual environment..."
    # shellcheck disable=SC1091
    source venv/bin/activate
else
    log_warn "No 'venv' folder found. Proceeding with system Python."
fi

require_command python
require_command python3

if [ ! -f "requirements.txt" ]; then
    log_error "requirements.txt not found in $(pwd)"
    exit 1
fi

install_python_requirements
install_playwright_browser

if [ ! -d "frontend" ]; then
    log_warn "frontend/ directory not found. Static dashboard will not be served."
fi

trap cleanup SIGINT SIGTERM

echo -e "${GREEN}[CORE]${NC} Starting API and Discord Bot..."
python main.py &
CORE_PID=$!

echo -e "${GREEN}[WORKER]${NC} Starting Automation Worker..."
python -m worker.main &
WORKER_PID=$!

if [ -d "frontend" ]; then
    echo -e "${GREEN}[WEB]${NC} Starting Dashboard at http://localhost:8080..."
    python3 -m http.server --directory frontend 8080 > /dev/null 2>&1 &
    WEB_PID=$!
fi

echo -e "${CYAN}---------------------------------------------${NC}"
echo -e "${GREEN}[SUCCESS]${NC} All systems are running."
echo -e "${YELLOW}[HINT]${NC} Press CTRL+C to stop everything at once."
echo -e "${CYAN}---------------------------------------------${NC}"

wait
