#!/bin/bash
# ============================================================================
# PROJECT RED SWORD - MOBILE TESTING C2 PANEL STARTUP
# ============================================================================
# Starts the mobile security testing command & control panel
# For in-house team iOS and Android security testing
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Navigate to project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Banner
echo -e "${RED}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   ███╗   ███╗ ██████╗ ██████╗ ██╗██╗     ███████╗                  ║
║   ████╗ ████║██╔═══██╗██╔══██╗██║██║     ██╔════╝                  ║
║   ██╔████╔██║██║   ██║██████╔╝██║██║     █████╗                    ║
║   ██║╚██╔╝██║██║   ██║██╔══██╗██║██║     ██╔══╝                    ║
║   ██║ ╚═╝ ██║╚██████╔╝██████╔╝██║███████╗███████╗                  ║
║   ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚═╝╚══════╝╚══════╝                  ║
║                                                                      ║
║         Mobile Testing C2 Panel - iOS & Android Testing             ║
║              In-House Security Team Assessment Tool                  ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${YELLOW}Starting Mobile Security Testing Infrastructure...${NC}\n"

# Check virtual environment
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found${NC}"
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo -e "${BLUE}[1/7] Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}\n"

# Install dependencies
echo -e "${BLUE}[2/7] Installing dependencies...${NC}"
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}\n"

# Check configuration
echo -e "${BLUE}[3/7] Checking configuration...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found${NC}"
    exit 1
fi

if [ ! -f "config/mobile_targets.yaml" ]; then
    echo -e "${YELLOW}⚠ mobile_targets.yaml not found${NC}"
    echo "   Please configure authorized targets in config/mobile_targets.yaml"
fi

source .env
echo -e "${GREEN}✓ Configuration loaded${NC}\n"

# Initialize database
echo -e "${BLUE}[4/7] Initializing database...${NC}"
python3 -c "from database.models import Base, engine; Base.metadata.create_all(bind=engine)" 2>/dev/null || echo "   Database already initialized"
echo -e "${GREEN}✓ Database ready${NC}\n"

# Create directories
echo -e "${BLUE}[5/7] Creating directories...${NC}"
mkdir -p logs reports/mobile_tests backups/mobile
echo -e "${GREEN}✓ Directories created${NC}\n"

# Check demo mode
echo -e "${BLUE}[6/7] Checking deployment mode...${NC}"
if [ "$DEMO_MODE" = "true" ]; then
    echo -e "${YELLOW}⚠ DEMO MODE: Enabled (safe simulations only)${NC}"
    echo "   - SMS messages will be simulated (not sent)"
    echo "   - Emails will be simulated (not sent)"
    echo "   - All actions logged for testing"
else
    echo -e "${CYAN}🔴 LIVE MODE: Real SMS/Email delivery enabled${NC}"
    echo "   - TextBelt SMS: $([ -n "$TEXTBELT_API_KEY" ] && echo "Configured ✓" || echo "Not configured ✗")"
    echo "   - SendGrid Email: $([ -n "$SENDGRID_API_KEY" ] && echo "Configured ✓" || echo "Not configured ✗")"
fi
echo ""

# Display authorized targets
echo -e "${BLUE}[7/7] Loading authorized targets...${NC}"
TARGET_COUNT=$(python3 -c "import yaml; f=open('config/mobile_targets.yaml'); d=yaml.safe_load(f); print(len(d.get('authorized_targets', [])))" 2>/dev/null || echo "0")
echo -e "   Authorized targets loaded: ${GREEN}${TARGET_COUNT}${NC}"
echo -e "${GREEN}✓ Targets loaded${NC}\n"

# Display information
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  MOBILE TESTING C2 PANEL STARTING${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "  ${YELLOW}C2 Panel URL:${NC}"
echo -e "    • Main Interface:   ${CYAN}http://localhost:5007${NC}"
echo -e "    • Health Check:     http://localhost:5007/api/health"
echo -e "    • Statistics API:   http://localhost:5007/api/stats"
echo ""
echo -e "  ${YELLOW}Testing Capabilities:${NC}"
echo -e "    • 📱 SMS Security Testing (iOS & Android)"
echo -e "    • 📧 Email Security Testing (iOS & Android)"
echo -e "    • 🎯 Phishing/Smishing Simulations"
echo -e "    • 🔐 Authorization Controls (targets whitelist)"
echo -e "    • 📊 Real-time Statistics"
echo -e "    • 📝 Comprehensive Logging"
echo ""
echo -e "  ${YELLOW}Safety Controls:${NC}"
echo -e "    • Demo Mode: ${DEMO_MODE:-true}"
echo -e "    • Authorization Required: YES"
echo -e "    • Activity Logging: ENABLED"
echo -e "    • Audit Trail: ENABLED"
echo ""
echo -e "  ${YELLOW}Configuration Files:${NC}"
echo -e "    • Targets: config/mobile_targets.yaml"
echo -e "    • Environment: .env"
echo -e "    • Logs: logs/mobile_testing.log"
echo ""
echo -e "  ${YELLOW}Quick Start:${NC}"
echo -e "    1. Open browser: http://localhost:5007"
echo -e "    2. Configure authorized targets in config/mobile_targets.yaml"
echo -e "    3. (Optional) Add Twilio/SendGrid credentials to .env for real testing"
echo -e "    4. Launch tests from the web interface"
echo ""
echo -e "  ${YELLOW}Emergency Stop:${NC}"
echo -e "    • Hotkey: ${RED}Ctrl+C${NC}"
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Start the C2 panel
python3 mobile_testing_c2_panel.py

# Cleanup on exit
echo ""
echo -e "${YELLOW}Shutting down Mobile Testing C2 Panel...${NC}"
echo -e "${GREEN}Shutdown complete${NC}"
