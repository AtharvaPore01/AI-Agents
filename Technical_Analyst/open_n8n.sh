#!/bin/bash

# Function to stop n8n when script exits
cleanup() {
    echo "Stopping n8n..."
    pkill -f "n8n start"  # Kill the n8n process
    exit 0
}

# Trap Ctrl+C (SIGINT) to stop n8n
trap cleanup SIGINT

# Start n8n in the background and save the process ID
n8n start > n8n_log.txt 2>&1 &
N8N_PID=$!

# Wait until n8n is fully started
echo "Waiting for n8n to be ready..."
while ! grep -q "Editor is now accessible via:" n8n_log.txt; do
    sleep 2
done

echo "n8n is running successfully!"

# Open n8n in Google Chrome
open -a "Google Chrome" http://localhost:5678

# Keep script running so that it can capture Ctrl+C to stop n8n
wait $N8N_PID
