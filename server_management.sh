#!/bin/bash
# Server Management Script for Project Red

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to start all servers
start_servers() {
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}   STARTING ALL SERVERS${NC}"
    echo -e "${GREEN}========================================${NC}"
    
    # Start Red Team Dashboard
    echo -e "\n${BLUE}[1/4]${NC} Starting Red Team Dashboard (Port 5008)..."
    python3 red_team_mobile_attack_dashboard.py > /tmp/red_team.log 2>&1 &
    RED_TEAM_PID=$!
    echo -e "      ${GREEN}✓${NC} Red Team PID: $RED_TEAM_PID"
    
    # Start Blue Team Dashboard
    echo -e "${BLUE}[2/4]${NC} Starting Blue Team Dashboard (Port 5009)..."
    python3 blue_team_monitoring_dashboard.py > /tmp/blue_team.log 2>&1 &
    BLUE_TEAM_PID=$!
    echo -e "      ${GREEN}✓${NC} Blue Team PID: $BLUE_TEAM_PID"
    
    # Start C2 Server
    echo -e "${BLUE}[3/4]${NC} Starting C2 Server (Port 4000)..."
    python3 c2_listener.py > /tmp/c2_server.log 2>&1 &
    C2_PID=$!
    echo -e "      ${GREEN}✓${NC} C2 Server PID: $C2_PID"
    
    # Start Control Panel
    echo -e "${BLUE}[4/4]${NC} Starting Control Panel Dashboard (Port 5010)..."
    python3 control_panel_dashboard.py > /tmp/control_panel.log 2>&1 &
    CONTROL_PID=$!
    echo -e "      ${GREEN}✓${NC} Control Panel PID: $CONTROL_PID"
    
    # Wait for servers to start
    echo -e "\n${YELLOW}Waiting for servers to initialize...${NC}"
    sleep 3
    
    # Check server status
    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}   SERVER STATUS${NC}"
    echo -e "${GREEN}========================================${NC}"
    
    check_port 5008 "Red Team Dashboard" "http://localhost:5008"
    check_port 5009 "Blue Team Dashboard" "http://localhost:5009"
    check_port 4000 "C2 Server" "http://localhost:4000"
    check_port 5010 "Control Panel" "http://localhost:5010"
    
    echo -e "\n${GREEN}✓ All servers started successfully!${NC}\n"
}

# Function to stop all servers
kill_servers() {
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}   STOPPING ALL SERVERS${NC}"
    echo -e "${RED}========================================${NC}\n"
    
    # Kill by process name
    echo -e "${YELLOW}Killing Red Team Dashboard...${NC}"
    pkill -9 -f "red_team_mobile_attack_dashboard.py"
    
    echo -e "${YELLOW}Killing Blue Team Dashboard...${NC}"
    pkill -9 -f "blue_team_monitoring_dashboard.py"
    
    echo -e "${YELLOW}Killing C2 Server...${NC}"
    pkill -9 -f "c2_listener.py"
    
    echo -e "${YELLOW}Killing Control Panel...${NC}"
    pkill -9 -f "control_panel_dashboard.py"
    
    sleep 1
    
    # Verify all stopped
    echo -e "\n${GREEN}Verifying all servers stopped...${NC}"
    
    if pgrep -f "red_team_mobile_attack_dashboard.py" > /dev/null; then
        echo -e "${RED}✗ Red Team still running${NC}"
    else
        echo -e "${GREEN}✓ Red Team stopped${NC}"
    fi
    
    if pgrep -f "blue_team_monitoring_dashboard.py" > /dev/null; then
        echo -e "${RED}✗ Blue Team still running${NC}"
    else
        echo -e "${GREEN}✓ Blue Team stopped${NC}"
    fi
    
    if pgrep -f "c2_listener.py" > /dev/null; then
        echo -e "${RED}✗ C2 Server still running${NC}"
    else
        echo -e "${GREEN}✓ C2 Server stopped${NC}"
    fi
    
    if pgrep -f "control_panel_dashboard.py" > /dev/null; then
        echo -e "${RED}✗ Control Panel still running${NC}"
    else
        echo -e "${GREEN}✓ Control Panel stopped${NC}"
    fi
    
    echo -e "\n${GREEN}✓ All servers stopped!${NC}\n"
}

# Function to restart all servers
restart_servers() {
    echo -e "${YELLOW}========================================${NC}"
    echo -e "${YELLOW}   RESTARTING ALL SERVERS${NC}"
    echo -e "${YELLOW}========================================${NC}\n"
    
    kill_servers
    sleep 2
    start_servers
}

# Function to check server status
status_servers() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}   SERVER STATUS CHECK${NC}"
    echo -e "${BLUE}========================================${NC}\n"
    
    check_port 5008 "Red Team Dashboard" "http://localhost:5008"
    check_port 5009 "Blue Team Dashboard" "http://localhost:5009"
    check_port 4000 "C2 Server" "http://localhost:4000"
    check_port 5010 "Control Panel" "http://localhost:5010"
    
    echo ""
}

# Helper function to check if port is listening
check_port() {
    PORT=$1
    NAME=$2
    URL=$3
    
    if ss -tlnp 2>/dev/null | grep -q ":$PORT "; then
        PID=$(ss -tlnp 2>/dev/null | grep ":$PORT " | grep -oP 'pid=\K[0-9]+' | head -1)
        echo -e "${GREEN}✓${NC} $NAME: ${GREEN}RUNNING${NC} (Port $PORT, PID: $PID)"
        echo -e "  URL: ${BLUE}$URL${NC}"
    else
        echo -e "${RED}✗${NC} $NAME: ${RED}STOPPED${NC} (Port $PORT)"
    fi
}

# Function to view logs
view_logs() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}   SERVER LOGS${NC}"
    echo -e "${BLUE}========================================${NC}\n"
    
    echo -e "${YELLOW}Select log to view:${NC}"
    echo -e "  1) Red Team Dashboard"
    echo -e "  2) Blue Team Dashboard"
    echo -e "  3) C2 Server"
    echo -e "  4) Control Panel"
    echo -e "  5) All logs (tail)"
    echo -e "  6) Back to menu"
    echo -e "\nChoice: "
    read -r choice
    
    case $choice in
        1) tail -50 /tmp/red_team.log ;;
        2) tail -50 /tmp/blue_team.log ;;
        3) tail -50 logs/c2_listener.log ;;
        4) tail -50 /tmp/control_panel.log ;;
        5) 
            echo -e "\n${GREEN}=== Red Team ===${NC}"
            tail -10 /tmp/red_team.log
            echo -e "\n${GREEN}=== Blue Team ===${NC}"
            tail -10 /tmp/blue_team.log
            echo -e "\n${GREEN}=== C2 Server ===${NC}"
            tail -10 logs/c2_listener.log
            echo -e "\n${GREEN}=== Control Panel ===${NC}"
            tail -10 /tmp/control_panel.log
            ;;
        *) return ;;
    esac
}

# Interactive menu
show_menu() {
    clear
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}   PROJECT RED - SERVER MANAGER${NC}"
    echo -e "${GREEN}========================================${NC}\n"
    echo -e "  ${BLUE}1)${NC} Start all servers"
    echo -e "  ${BLUE}2)${NC} Stop all servers"
    echo -e "  ${BLUE}3)${NC} Restart all servers"
    echo -e "  ${BLUE}4)${NC} Check server status"
    echo -e "  ${BLUE}5)${NC} View logs"
    echo -e "  ${BLUE}6)${NC} Exit"
    echo -e "\n${YELLOW}Enter your choice [1-6]:${NC} "
}

# Main script logic
if [ "$1" == "start" ]; then
    start_servers
elif [ "$1" == "stop" ] || [ "$1" == "kill" ]; then
    kill_servers
elif [ "$1" == "restart" ]; then
    restart_servers
elif [ "$1" == "status" ]; then
    status_servers
elif [ "$1" == "logs" ]; then
    view_logs
else
    # Interactive mode
    while true; do
        show_menu
        read -r choice
        case $choice in
            1) start_servers; read -p "Press Enter to continue..." ;;
            2) kill_servers; read -p "Press Enter to continue..." ;;
            3) restart_servers; read -p "Press Enter to continue..." ;;
            4) status_servers; read -p "Press Enter to continue..." ;;
            5) view_logs; read -p "Press Enter to continue..." ;;
            6) echo -e "\n${GREEN}Goodbye!${NC}\n"; exit 0 ;;
            *) echo -e "${RED}Invalid option!${NC}"; sleep 1 ;;
        esac
    done
fi
