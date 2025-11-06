#!/bin/bash
# ============================================================================
# NETWORK ATTACK LAUNCHER
# ============================================================================
# Simple script to launch network exploitation simulations
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
echo -e "${RED}║       NETWORK EXPLOITATION SIMULATION LAUNCHER                  ║${NC}"
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
echo -e "${BLUE}Available network attacks:${NC}"
echo "  1) DNS Tunneling"
echo "  2) ICMP Tunneling"
echo "  3) TCP/IP Stack Exploitation"
echo ""
read -p "Select attack type (1-3) or press Enter for random: " choice

case $choice in
    1) attack_method="dns_tunneling" ;;
    2) attack_method="icmp_tunneling" ;;
    3) attack_method="tcp_ip_stack_exploitation" ;;
    *) attack_method="random" ;;
esac

echo ""
read -p "Enter target IP (or press Enter for default): " target
target=${target:-"192.168.100.10"}

echo ""
echo -e "${YELLOW}Launching network exploitation...${NC}"
echo -e "  Attack Method: $attack_method"
echo -e "  Target: $target"
echo ""

# Run the network exploitation
python3 << EOF
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from modules.network_exploitation import NetworkExploitation
import random

print("=" * 70)
print("  NETWORK EXPLOITATION STARTING")
print("=" * 70)
print()

net = NetworkExploitation()

attack_method = "$attack_method"
target = "$target"

# If random, pick one
if attack_method == "random":
    attack_method = random.choice(net.exploitation_methods)
    print(f"Randomly selected: {attack_method}")
    print()

result = net.exploit_network(attack_method, target)

print()
print("=" * 70)
print("  ATTACK RESULT")
print("=" * 70)
print()
print(result)
print()
print("=" * 70)
print("  NETWORK EXPLOITATION COMPLETED")
print("=" * 70)
EOF

echo ""
echo -e "${GREEN}✓ Network exploitation completed${NC}"
echo -e "${YELLOW}Check logs: tail -f logs/attack_simulation.log${NC}"
echo ""
