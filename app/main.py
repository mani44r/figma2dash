"""
FastAPI Web Application
Main web server with API endpoints and UI for Figma to Dashboard conversion.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.models import FigmaRequest
from app.pipeline import ProcessingPipeline

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Figma to Dashboard Generator",
    description="AI-powered tool to convert Figma designs into dashboard configurations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates
templates = Jinja2Templates(directory="app/templates")

# Static files (if needed later)
# app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main UI."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/convert")
async def convert_figma(request: FigmaRequest):
    """
    Convert a Figma design to dashboard config.
    
    POST body: {"figma_url": "https://www.figma.com/..."}
    Returns: JSON dashboard configuration
    """
    try:
        # Validate environment
        if not os.getenv("FIGMA_TOKEN"):
            raise HTTPException(
                status_code=500,
                detail="FIGMA_TOKEN not configured. Please set it in .env file."
            )
        
        if not os.getenv("GEMINI_API_KEY"):
            raise HTTPException(
                status_code=500,
                detail="GEMINI_API_KEY not configured. Please set it in .env file."
            )
        
        # Run pipeline
        pipeline = ProcessingPipeline(request.figma_url)
        config = pipeline.run()
        
        # Return results
        return JSONResponse(content={
            "success": True,
            "summary": pipeline.get_summary(),
            "config_json": pipeline.get_json(pretty=True),
            "config_yaml": pipeline.get_yaml(),
        })
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except EnvironmentError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    env_status = {
        "figma_token_set": bool(os.getenv("FIGMA_TOKEN")),
        "gemini_key_set": bool(os.getenv("GEMINI_API_KEY")),
    }
    
    all_configured = all(env_status.values())
    
    return {
        "status": "healthy" if all_configured else "misconfigured",
        "environment": env_status
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
