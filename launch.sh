#!/bin/bash

# CHRIZ__3656 AI - Unified Launch Script

# 1. Colors for logging
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}=============================================${NC}"
echo -e "${CYAN}      CHRIZ__3656 AI PLATFORM LAUNCHER      ${NC}"
echo -e "${CYAN}=============================================${NC}"

# 2. Check for Virtual Environment
if [ -d "venv" ]; then
    echo -e "${GREEN}[INFO]${NC} Activating virtual environment..."
    source venv/bin/activate
else
    echo -e "${YELLOW}[WARN]${NC} No 'venv' folder found. Proceeding with system python..."
fi

# 3. Trap to kill background processes on exit (CTRL+C)
cleanup() {
    echo -e "\n${RED}[SHUTDOWN]${NC} Stopping all services..."
    kill $(jobs -p)
    exit
}
trap cleanup SIGINT

# 4. Start Core API & Discord Bot
echo -e "${GREEN}[CORE]${NC} Starting API and Discord Bot..."
python main.py &
CORE_PID=$!

# 5. Start Automation Worker
echo -e "${GREEN}[WORKER]${NC} Starting Automation Worker..."
python -m worker.main &
WORKER_PID=$!

# 6. Start Frontend Server (Optional, but helpful)
echo -e "${GREEN}[WEB]${NC} Starting Dashboard at http://localhost:8080..."
python3 -m http.server --directory frontend 8080 > /dev/null 2>&1 &
WEB_PID=$!

echo -e "${CYAN}---------------------------------------------${NC}"
echo -e "${GREEN}[SUCCESS]${NC} All systems are running."
echo -e "${YELLOW}[HINT]${NC} Press CTRL+C to stop everything at once."
echo -e "${CYAN}---------------------------------------------${NC}"

# Wait for background processes
wait
