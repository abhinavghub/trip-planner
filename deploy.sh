#!/bin/bash

echo "🚀 Preparing Trip Planner for Railway Deployment..."

# Build the frontend
echo "📦 Building React frontend..."
cd frontend/trip-planner-frontend
npm run build
cd ../..

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📥 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway (if not already logged in)
echo "🔐 Logging into Railway..."
railway login

# Initialize Railway project
echo "🚂 Initializing Railway project..."
railway init

# Deploy to Railway
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment complete!"
echo "🌐 Your app will be available at the URL shown above"
echo "📝 Don't forget to update the frontend config with your backend URL" 