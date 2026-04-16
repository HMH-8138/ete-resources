#!/bin/bash
# Deploy backend to PythonAnywhere
# Usage: ./deploy-backend.sh YOUR_USERNAME YOUR_API_TOKEN

PYTHONANYWHERE_USERNAME=$1
API_TOKEN=$2

if [ -z "$PYTHONANYWHERE_USERNAME" ] || [ -z "$API_TOKEN" ]; then
    echo "Usage: ./deploy-backend.sh YOUR_USERNAME YOUR_API_TOKEN"
    echo ""
    echo "To get your API token:"
    echo "1. Log in to PythonAnywhere"
    echo "2. Go to Account → API token"
    echo "3. Copy your token"
    exit 1
fi

echo "Deploying backend to PythonAnywhere..."
echo "Username: $PYTHONANYWHERE_USERNAME"

# Create deployment package
cd my-backend
zip -r backend-deploy.zip . -x "node_modules/*" "uploads/*" ".env*"

echo "Uploading to PythonAnywhere..."
# You can use PythonAnywhere API or manual upload
# For manual upload: go to PythonAnywhere web interface and upload the zip

echo "✅ Backend package created: my-backend/backend-deploy.zip"
echo "📤 Upload this file to PythonAnywhere via web interface"
echo "📖 Then extract and run: npm install && npm start"
