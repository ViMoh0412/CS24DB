#!/bin/bash
# CS24DB Railway Deployment Script
# Run this in your terminal: bash deploy.sh

set -e

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

echo "=== CS24DB Railway Deployment ==="
echo ""

# Step 1: Login
echo "Step 1: Logging into Railway..."
railway login
echo ""

# Step 2: Link to existing project
echo "Step 2: Linking to your CS24DB project..."
echo ">> Select your CS24DB project and environment when prompted"
railway link
echo ""

# Step 3: Deploy
echo "Step 3: Deploying..."
railway up --detach
echo ""

echo "=== Deployment triggered! ==="
echo "Step 4: Generate a public domain:"
echo "  railway domain"
echo ""
echo "Or go to Railway Dashboard → your service → Settings → Networking → Generate Domain"
