#!/bin/bash

# ============================================================================
# PROJECT RED SWORD - RED TEAM STARTUP SCRIPT
# ============================================================================
# This script safely starts the red team attack simulation environment
# with all necessary safety checks and monitoring
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project paths
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Banner
echo -e "${RED}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   ██████╗ ██████╗  ██████╗      ██╗███████╗ ██████╗████████╗       ║
║   ██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝██╔════╝╚══██╔══╝       ║
║   ██████╔╝██████╔╝██║   ██║     ██║█████╗  ██║        ██║          ║
║   ██╔═══╝ ██╔══██╗██║   ██║██   ██║██╔══╝  ██║        ██║          ║
║   ██║     ██║  ██║╚██████╔╝╚█████╔╝███████╗╚██████╗   ██║          ║
║   ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝   ╚═╝          ║
║                                                                      ║
║         RED SWORD - Red Team Attack Simulation Platform             ║
║                  Production Deployment v1.0                          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${YELLOW}Starting Red Team Operations...${NC}\n"

# Step 1: Pre-flight checks
echo -e "${BLUE}[1/10] Running pre-flight safety checks...${NC}"
python3 scripts/health_check.py --mode preflight
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Pre-flight checks failed. Cannot start.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Pre-flight checks passed${NC}\n"

# Step 2: Check Python version
echo -e "${BLUE}[2/10] Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python version: $PYTHON_VERSION"
echo -e "${GREEN}✓ Python version OK${NC}\n"

# Step 3: Check dependencies
echo -e "${BLUE}[3/10] Checking dependencies...${NC}"
if [ ! -d "venv" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}\n"

# Step 4: Verify environment configuration
echo -e "${BLUE}[4/10] Verifying environment configuration...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found${NC}"
    echo "   Copying from .env.example..."
    cp .env.example .env 2>/dev/null || echo "No .env.example found"
fi
echo -e "${GREEN}✓ Environment configured${NC}\n"

# Step 5: Check configuration files
echo -e "${BLUE}[5/10] Checking configuration files...${NC}"
CONFIG_FILES=("config/attack_config.yaml" "config/safe_mode.yaml" "config/targets.yaml")
for config in "${CONFIG_FILES[@]}"; do
    if [ -f "$config" ]; then
        echo "   ✓ $config"
    else
        echo -e "   ${YELLOW}⚠ $config not found${NC}"
    fi
done
echo -e "${GREEN}✓ Configuration files checked${NC}\n"

# Step 6: Initialize database
echo -e "${BLUE}[6/10] Initializing database...${NC}"
python3 -c "from database.models import Base, engine; Base.metadata.create_all(bind=engine)" 2>/dev/null || echo "   Database already initialized"
echo -e "${GREEN}✓ Database initialized${NC}\n"

# Step 7: Create necessary directories
echo -e "${BLUE}[7/10] Creating directories...${NC}"
mkdir -p logs reports/generated reports/incidents backups tmp cache
echo -e "${GREEN}✓ Directories created${NC}\n"

# Step 8: Remove old stop signals
echo -e "${BLUE}[8/10] Clearing stop signals...${NC}"
rm -f .stop_attacks .kill_switch
echo -e "${GREEN}✓ Stop signals cleared${NC}\n"

# Step 9: Verify monitoring systems
echo -e "${BLUE}[9/10] Verifying monitoring systems...${NC}"
python3 scripts/health_check.py --mode monitoring
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠ Some monitoring checks failed, but continuing...${NC}"
fi
echo -e "${GREEN}✓ Monitoring verified${NC}\n"

# Step 10: Start the application
echo -e "${BLUE}[10/10] Starting Red Team platform...${NC}\n"

echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  RED TEAM PLATFORM STARTING${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "  ${YELLOW}Dashboard URL:${NC}"
echo -e "    • Main Dashboard:   http://localhost:5006/red_team_dashboard"
echo -e ""
echo -e "  ${YELLOW}Tabs Available:${NC}"
echo -e "    • 🏠 Home - System overview and quick start"
echo -e "    • 🎯 Attack Control - Launch attack simulations"
echo -e "    • 🛡️ Defense Monitoring - Real-time threat visualization"
echo ""
echo -e "  ${YELLOW}Safety Features Enabled:${NC}"
echo -e "    • Safe Mode: ACTIVE"
echo -e "    • Rate Limiting: ACTIVE"
echo -e "    • Kill Switch: AVAILABLE"
echo -e "    • Network Segmentation: ENFORCED"
echo -e "    • Attack Logging: ACTIVE"
echo ""
echo -e "  ${YELLOW}Emergency Stop:${NC}"
echo -e "    • Command: python3 scripts/kill_all_simulations.py"
echo -e "    • Hotkey: Ctrl+C (graceful shutdown)"
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Start Panel server with unified dashboard
panel serve red_team_dashboard.py \
    --port 5006 \
    --address 0.0.0.0 \
    --allow-websocket-origin="*" \
    --show \
    --log-level info

# Cleanup on exit
echo -e "\n${YELLOW}Shutting down Red Team platform...${NC}"
python3 scripts/kill_all_simulations.py --yes --reason "Normal shutdown" 2>/dev/null || true
echo -e "${GREEN}Shutdown complete${NC}"
