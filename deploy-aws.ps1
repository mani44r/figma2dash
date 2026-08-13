# AWS Elastic Beanstalk Deployment Script for Windows
# Run this script to deploy to AWS

Write-Host "🚀 Deploying Figma to Dashboard to AWS Elastic Beanstalk..." -ForegroundColor Green

# Check if EB CLI is installed
try {
    $ebVersion = eb --version 2>&1
    Write-Host "✅ AWS EB CLI is installed: $ebVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS EB CLI not installed. Installing..." -ForegroundColor Yellow
    pip install awsebcli
}

# Load environment variables from .env
if (Test-Path .env) {
    Get-Content .env | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            $name = $matches[1]
            $value = $matches[2]
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
}

# Initialize EB (first time only)
if (-not (Test-Path ".elasticbeanstalk")) {
    Write-Host "📦 Initializing Elastic Beanstalk..." -ForegroundColor Cyan
    eb init -p python-3.12 figma-to-dashboard --region us-east-1
}

# Check if environment exists
$envExists = eb list 2>&1 | Select-String "figma-to-dashboard-env"

if (-not $envExists) {
    Write-Host "🌍 Creating new environment..." -ForegroundColor Cyan
    eb create figma-to-dashboard-env --instance-type t3.micro --single
    
    # Set environment variables
    Write-Host "🔐 Setting environment variables..." -ForegroundColor Cyan
    $figmaToken = $env:FIGMA_TOKEN
    $geminiKey = $env:GEMINI_API_KEY
    eb setenv FIGMA_TOKEN=$figmaToken GEMINI_API_KEY=$geminiKey
} else {
    Write-Host "📤 Deploying to existing environment..." -ForegroundColor Cyan
    eb deploy
}

# Open the application
Write-Host "✅ Deployment complete!" -ForegroundColor Green
eb open
