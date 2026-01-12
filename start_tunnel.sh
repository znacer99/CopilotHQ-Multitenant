#!/bin/bash

# Check if npx is installed
if ! command -v npx &> /dev/null; then
    echo "❌ npx is not installed. Please install Node.js (with npm) first."
    exit 1
fi

echo "🚀 Starting Local Tunnel for n8n..."
echo "-----------------------------------"
echo "NOTE: When the tunnel starts, it will give you a URL (e.g., https://wild-dog-42.loca.lt)"
echo "You MUST copy that URL and update your .env file or export it as WEBHOOK_URL"
echo "Example: export WEBHOOK_URL=https://wild-dog-42.loca.lt"
echo "-----------------------------------"
echo ""

# Try to use a consistent subdomain based on user name or random consistent string
SUBDOMAIN="copilothq-local-$(whoami)"

echo "Attempting to claim subdomain: $SUBDOMAIN"
npx localtunnel --port 5678 --subdomain "$SUBDOMAIN"

# Fallback if subdomain is taken
if [ $? -ne 0 ]; then
    echo "⚠️  Subdomain taken or error. Starting with random subdomain..."
    npx localtunnel --port 5678
fi
