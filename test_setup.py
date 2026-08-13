"""
Setup Test Script
Verifies that all dependencies and environment variables are configured correctly.
"""

import sys
from dotenv import load_dotenv

print("=" * 60)
print("🧪 Testing Figma to Dashboard Setup")
print("=" * 60)

# Load environment
load_dotenv()
print("\n✅ Loaded .env file")

# Test 1: Check Python version
print("\n[1/6] Checking Python version...")
version = sys.version_info
if version.major >= 3 and version.minor >= 10:
    print(f"    ✅ Python {version.major}.{version.minor}.{version.micro}")
else:
    print(f"    ❌ Python {version.major}.{version.minor}.{version.micro} (need 3.10+)")
    sys.exit(1)

# Test 2: Check dependencies
print("\n[2/6] Checking dependencies...")
try:
    import fastapi
    import uvicorn
    import httpx
    import openai
    import pydantic
    import yaml
    from PIL import Image
    print("    ✅ All dependencies installed")
except ImportError as e:
    print(f"    ❌ Missing dependency: {e}")
    print("    Run: pip install -r requirements.txt")
    sys.exit(1)

# Test 3: Check environment variables
print("\n[3/6] Checking environment variables...")
import os

figma_token = os.getenv("FIGMA_TOKEN", "")
openai_key = os.getenv("OPENAI_API_KEY", "")

if figma_token:
    print(f"    ✅ FIGMA_TOKEN set ({figma_token[:10]}...)")
else:
    print("    ❌ FIGMA_TOKEN not set")
    print("    Add to .env file: FIGMA_TOKEN=your_token_here")

if openai_key:
    print(f"    ✅ OPENAI_API_KEY set ({openai_key[:10]}...)")
else:
    print("    ❌ OPENAI_API_KEY not set")
    print("    Add to .env file: OPENAI_API_KEY=your_key_here")

if not figma_token or not openai_key:
    print("\n⚠️  Missing API credentials. Please configure .env file.")
    sys.exit(1)

# Test 4: Test Figma API connection
print("\n[4/6] Testing Figma API connection...")
try:
    from app.figma.client import get_token
    token = get_token()
    
    import httpx
    response = httpx.get(
        "https://api.figma.com/v1/me",
        headers={"X-Figma-Token": token},
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"    ✅ Connected as: {data.get('email', 'Unknown')}")
    else:
        print(f"    ❌ API returned status {response.status_code}")
        print("    Check your FIGMA_TOKEN")
except Exception as e:
    print(f"    ❌ Connection failed: {e}")

# Test 5: Test OpenAI API connection
print("\n[5/6] Testing OpenAI API connection...")
try:
    from app.classifier.vision_classifier import get_openai_client
    client = get_openai_client()
    
    # Simple API test (doesn't use credits)
    models = client.models.list()
    print(f"    ✅ Connected to OpenAI API")
    print(f"    Available models: {len(list(models.data))} found")
except Exception as e:
    print(f"    ❌ Connection failed: {e}")
    print("    Check your OPENAI_API_KEY and account status")

# Test 6: Test app can be imported
print("\n[6/6] Testing application modules...")
try:
    from app.main import app
    from app.pipeline import ProcessingPipeline
    from app.models import DashboardConfig
    print("    ✅ All modules imported successfully")
except Exception as e:
    print(f"    ❌ Import failed: {e}")
    sys.exit(1)

# Success!
print("\n" + "=" * 60)
print("✅ Setup verification complete!")
print("=" * 60)
print("\n🚀 Next steps:")
print("   1. Run: python app/main.py")
print("   2. Open: http://localhost:8000")
print("   3. Paste a Figma URL and convert!")
print("\n💡 Or run: run.bat (Windows)")
print()
