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
from .pdf_extractor import extract_text_from_pdf
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
    description="API for extracting text from medical PDFs and generating summaries with action items and deficiencies",
    version="1.0.0"
)

@app.post("/upload", summary="Upload a medical PDF report for summarization")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file, extract text, and generate summary, action items, and deficiencies.
    
    Args:
        file: The PDF file to process
        
    Returns:
        JSON response with summary, action_items, and deficiencies
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Create a temporary directory to store the uploaded file
    temp_dir = tempfile.mkdtemp()
    try:
        # Save the uploaded file to a temporary location
        temp_file_path = os.path.join(temp_dir, file.filename)
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Saved uploaded file to {temp_file_path}")
        
        # Extract text from PDF
        text = extract_text_from_pdf(temp_file_path)
        if text is None:
            logger.error("Failed to extract text from PDF")
            raise HTTPException(status_code=500, detail="Failed to extract text from PDF")
        
        logger.info(f"Extracted {len(text)} characters of text")
        
        # Generate summary and analysis
        result = summarize_medical_report(text)
        
        # Return the result
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
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
