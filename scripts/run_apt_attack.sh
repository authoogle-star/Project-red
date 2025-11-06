#!/bin/bash
# ============================================================================
# APT ATTACK LAUNCHER
# ============================================================================
# Simple script to launch APT (Advanced Persistent Threat) simulations
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Navigate to project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${RED}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${RED}║           APT SIMULATION ATTACK LAUNCHER                        ║${NC}"
echo -e "${RED}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source venv/bin/activate
else
    echo -e "${RED}❌ Virtual environment not found. Run ./scripts/start_red_team.sh first.${NC}"
    exit 1
fi

# Check safe mode
echo -e "${YELLOW}Checking safe mode...${NC}"
if [ -f ".env" ]; then
    source .env
    if [ "$SAFE_MODE" = "true" ]; then
        echo -e "${GREEN}✓ Safe mode: ENABLED${NC}"
    else
        echo -e "${RED}⚠ Safe mode: DISABLED - Proceeding with caution${NC}"
    fi
fi

echo ""
echo -e "${YELLOW}Launching APT simulation...${NC}"
echo ""

# Run the APT simulation
python3 << 'EOF'
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from modules.apt_simulation import APTSimulation
import json

print("=" * 70)
print("  APT SIMULATION STARTING")
print("=" * 70)
print()

apt = APTSimulation()
result = apt.simulate_attack()

print()
print("=" * 70)
print("  ATTACK RESULT")
print("=" * 70)
print()
print(result)
print()
print("=" * 70)
print("  APT SIMULATION COMPLETED")
print("=" * 70)
EOF

echo ""
echo -e "${GREEN}✓ APT simulation completed${NC}"
echo -e "${YELLOW}Check logs: tail -f logs/attack_simulation.log${NC}"
echo ""
