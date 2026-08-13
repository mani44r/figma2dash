@echo off
echo ========================================
echo Figma to Dashboard Generator
echo ========================================
echo.
echo Starting FastAPI server...
echo Open your browser to: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
