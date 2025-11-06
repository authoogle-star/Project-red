#!/bin/bash
# ============================================================================
# PHISHING ATTACK LAUNCHER
# ============================================================================
# Simple script to launch phishing attack simulations
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Navigate to project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${RED}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${RED}║        PHISHING ATTACK SIMULATION LAUNCHER                      ║${NC}"
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

# Show attack options
echo ""
echo -e "${BLUE}Available phishing attacks:${NC}"
echo "  1) Standard Phishing"
echo "  2) Spear Phishing (targeted)"
echo "  3) Whaling (executive targeted)"
echo ""
read -p "Select attack type (1-3) or press Enter for random: " choice

case $choice in
    1) attack_type="phishing" ;;
    2) attack_type="spear_phishing" ;;
    3) attack_type="whaling" ;;
    *) attack_type="random" ;;
esac

echo ""
read -p "Enter target (or press Enter for default target): " target
target=${target:-"test-user@example.com"}

echo ""
echo -e "${YELLOW}Launching phishing simulation...${NC}"
echo -e "  Attack Type: $attack_type"
echo -e "  Target: $target"
echo ""

# Run the phishing simulation
python3 << EOF
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from modules.advanced_social_engineering import AdvancedSocialEngineering
import random

print("=" * 70)
print("  PHISHING SIMULATION STARTING")
print("=" * 70)
print()

se = AdvancedSocialEngineering()

attack_type = "$attack_type"
target = "$target"

# If random, pick one
if attack_type == "random":
    attack_type = random.choice(["phishing", "spear_phishing", "whaling"])
    print(f"Randomly selected: {attack_type}")
    print()

result = se.execute_attack(attack_type, target)

print()
print("=" * 70)
print("  ATTACK RESULT")
print("=" * 70)
print()
print(result)
print()
print("=" * 70)
print("  PHISHING SIMULATION COMPLETED")
print("=" * 70)
EOF

echo ""
echo -e "${GREEN}✓ Phishing simulation completed${NC}"
echo -e "${YELLOW}Check logs: tail -f logs/attack_simulation.log${NC}"
echo ""
