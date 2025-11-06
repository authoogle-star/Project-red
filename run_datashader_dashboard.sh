#!/bin/bash

# Datashader Security Monitoring Dashboard Launcher
# Project Red-Sword

echo "╔══════════════════════════════════════════════════════╗"
echo "║  Datashader Security Monitoring Dashboard          ║"
echo "║  Project Red-Sword                                  ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Check if required packages are installed
echo "[1/4] Checking dependencies..."

python3 -c "import datashader" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Datashader not found. Installing dependencies..."
    pip install -r requirements.txt
else
    echo "✅ Dependencies verified"
fi

echo ""
echo "[2/4] Verifying Panel installation..."
python3 -c "import panel" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Panel not found. Installing..."
    pip install panel
else
    echo "✅ Panel is installed"
fi

echo ""
echo "[3/4] Starting Datashader dashboard..."
echo ""
echo "🌐 Dashboard will be available at:"
echo "   - Image Classification:  http://localhost:5006/Panel_Demo_-_Image_Classification"
echo "   - Datashader Monitoring: http://localhost:5006/Datashader_Security_Monitoring"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Panel server
echo "[4/4] Launching..."
panel serve app.py --show --port 5006 --allow-websocket-origin="*"
