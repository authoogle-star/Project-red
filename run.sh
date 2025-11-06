#!/bin/bash
# Script to run the Panel application

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the Panel application
echo "Starting Panel application..."
echo "Access the app at: http://localhost:5006"
panel serve app.py --show --autoreload
