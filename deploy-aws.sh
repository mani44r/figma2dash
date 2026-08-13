#!/bin/bash

# AWS Elastic Beanstalk Deployment Script
# Run this script to deploy to AWS

echo "🚀 Deploying Figma to Dashboard to AWS Elastic Beanstalk..."

# Check if EB CLI is installed
if ! command -v eb &> /dev/null
then
    echo "❌ AWS EB CLI not installed. Installing..."
    pip install awsebcli
fi

# Initialize EB (first time only)
if [ ! -d ".elasticbeanstalk" ]; then
    echo "📦 Initializing Elastic Beanstalk..."
    eb init -p python-3.12 figma-to-dashboard --region us-east-1
fi

# Create environment (first time only) or deploy
if ! eb list | grep -q "figma-to-dashboard-env"; then
    echo "🌍 Creating new environment..."
    eb create figma-to-dashboard-env --instance-type t3.micro --single
    
    # Set environment variables
    echo "🔐 Setting environment variables..."
    eb setenv FIGMA_TOKEN=$FIGMA_TOKEN GEMINI_API_KEY=$GEMINI_API_KEY
else
    echo "📤 Deploying to existing environment..."
    eb deploy
fi

# Open the application
echo "✅ Deployment complete!"
eb open
