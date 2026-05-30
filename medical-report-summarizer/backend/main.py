#!/usr/bin/env python3
"""
FastAPI backend for the Medical Report Summarizer.
"""

import os
import logging
import tempfile
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Import our local modules
from .pdf_extractor import extract_text_from_file
from .summarizer import summarize_medical_report

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Medical Report Summarizer API",
    description="API for extracting text from medical PDFs and images and generating summaries with action items and deficiencies",
    version="1.0.0"
)

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp'}

def allowed_file(filename: str) -> bool:
    """Check if the file has an allowed extension."""
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

@app.post("/upload", summary="Upload a medical PDF or image file for summarization")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file (PDF or image), extract text, and generate summary, action items, and deficiencies.
    
    Args:
        file: The file to process
        
    Returns:
        JSON response with summary, action_items, and deficiencies
    """
    # Validate file type
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Create a temporary directory to store the uploaded file
    temp_dir = tempfile.mkdtemp()
    try:
        # Save the uploaded file to a temporary location
        temp_file_path = os.path.join(temp_dir, file.filename)
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Saved uploaded file to {temp_file_path}")
        
        # Extract text from file
        text = extract_text_from_file(temp_file_path)
        if text is None:
            logger.error("Failed to extract text from file")
            raise HTTPException(status_code=500, detail="Failed to extract text from file")
        
        logger.info(f"Extracted {len(text)} characters of text")
        
        # Generate summary and analysis
        result = summarize_medical_report(text)
        
        # Return the result
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)

@app.get("/health", summary="Health check endpoint")
async def health_check():
    """Simple health check to verify the API is running."""
    return {"status": "healthy", "service": "medical-report-summarizer"}

if __name__ == "__main__":
    # This is for development only; use uvicorn for production
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
