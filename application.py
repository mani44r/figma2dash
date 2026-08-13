"""
AWS Elastic Beanstalk Entry Point
This file is required for Elastic Beanstalk to recognize the ASGI application.
"""

from app.main import app

# Elastic Beanstalk looks for 'application' variable
application = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(application, host="0.0.0.0", port=8000)
