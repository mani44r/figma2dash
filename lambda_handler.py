"""
AWS Lambda Handler for Serverless Deployment
Uses Mangum to adapt FastAPI for Lambda
"""

from mangum import Mangum
from app.main import app

# Lambda handler
handler = Mangum(app, lifespan="off")
